Copyright ©2017,.  The University of Chicago (“Chicago”). All Rights Reserved.  

Permission to use, copy, modify, and distribute this software, including all object code and source code, and any accompanying documentation (together the “Program”) for educational and not-for-profit research purposes, without fee and without a signed licensing agreement, is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies, modifications, and distributions. For the avoidance of doubt, educational and not-for-profit research purposes excludes any service or part of selling a service that uses the Program. To obtain a commercial license for the Program, contact the Technology Commercialization and Licensing, Polsky Center for Entrepreneurship and Innovation, University of Chicago, 1452 East 53rd Street, 2nd floor, Chicago, IL 60615.

Created by Data Science and Public Policy, University of Chicago

The Program is copyrighted by Chicago. The Program is supplied "as is", without any accompanying services from Chicago. Chicago does not warrant that the operation of the Program will be uninterrupted or error-free. The end-user understands that the Program was developed for research purposes and is advised not to rely exclusively on the Program for any reason.

IN NO EVENT SHALL CHICAGO BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THE PROGRAM, EVEN IF CHICAGO HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. CHICAGO SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE PROGRAM PROVIDED HEREUNDER IS PROVIDED "AS IS". CHICAGO HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

Description: # Catwalk
        
        Training, testing, and evaluating machine learning classifier models
        
        [![Build Status](https://travis-ci.org/dssg/catwalk.svg?branch=master)](https://travis-ci.org/dssg/catwalk)
        [![codecov](https://codecov.io/gh/dssg/catwalk/branch/master/graph/badge.svg)](https://codecov.io/gh/dssg/catwalk)
        [![codeclimate](https://codeclimate.com/github/dssg/catwalk.png)](https://codeclimate.com/github/dssg/catwalk)
        
        At the core of many predictive analytics applications is the need to train classifiers on large set of design matrices, test and temporally cross-validate them, and generate evaluation metrics about them.
        
        Python's scikit-learn package provides much of this functionality, but it is not trivial to design large experiments with it in a persistable way . Catwalk builds upon the functionality offered by scikit-learn by implementing:
        
        - Saving of modeling results and metadata in a [Postgres database](https://github.com/dssg/results-schema) for later analysis
        - Exposure of computationally-intensive tasks as discrete workloads that can be used with different parallelization solutions (e.g. multiprocessing, Celery)
        - Different model persistence strategies such as on-filesystem or Amazon S3, that can be easily switched between
        - Hashing classifier model configuration to only retrain a model if necessary.
        - Various best practices in areas like input scaling for different classifier types and feature importance
        - Common scikit-learn model evaluation metrics as well as the ability to bundle custom evaluation metrics
        
        
        ## Components
        
        This functionality is concentrated in the following components:
        
        - [catwalk.ModelTrainer](catwalk/model_trainers.py): Train a configured experiment grid on pre-made design matrices, and store each model's metadata and feature importances in a database.
        - [catwalk.Predictor](catwalk/predictors.py): Given a trained model and another matrix (ie, a test matrix), generate prediction probabilities and store them in a database.
        - [catwalk.ModelEvaluator](catwalk/evaluation.py): Given a set of model prediction probabilities, generate metrics (for instance, precision and recall at various thresholds) and store them in a database.
        
        ## Usage
        
        Below is a complete sample usage of the three Catwalk components.
        
        ```
        
        import datetime
        
        import pandas
        from sqlalchemy import create_engine
        
        from metta import metta_io as metta
        
        from catwalk.storage import FSModelStorageEngine, MettaCSVMatrixStore
        from catwalk.model_trainers import ModelTrainer
        from catwalk.predictors import Predictor
        from catwalk.evaluation import ModelEvaluator
        from catwalk.utils import save_experiment_and_get_hash
        
        
        # create a sqlalchemy database engine pointing to a Postgres database
        db_engine = create_engine(...)
        
        # A path on your filesystem under which to store matrices and models
        project_path = 'mytestproject/modeling'
        
        # create a toy train matrix from scratch
        # and saving it using metta to generate a unique id for its metadata
        # catwalk uses both the matrix and metadata
        train_matrix = pandas.DataFrame.from_dict({
        	'entity_id': [1, 2],
        	'feature_one': [3, 4],
        	'feature_two': [5, 6],
        	'label': [7, 8]
        }).set_index('entity_id')
        train_metadata = {
        	'beginning_of_time': datetime.date(2012, 12, 20),
        	'end_time': datetime.date(2016, 12, 20),
        	'label_name': 'label',
        	'label_window': '1y',
        	'feature_names': ['ft1', 'ft2'],
        }
        train_matrix_uuid = metta.archive_matrix(train_metadata, train_matrix, format='csv')
        
        # The MettaCSVMatrixStore bundles the matrix and metadata together
        # for catwalk to use
        train_matrix_store = MettaCSVMatrixStore(
        	matrix_path='{}.csv'.format(train_matrix_uuid),
        	metadata_path='{}.yaml'.format(train_matrix_uuid)
        )
        
        
        # Similarly, create a test matrix
        as_of_date = datetime.date(2016, 12, 21)
        
        test_matrix = pandas.DataFrame.from_dict({
        	'entity_id': [3],
        	'feature_one': [8],
        	'feature_two': [5],
        	'label': [5]
        }).set_index('entity_id')
        
        test_metadata = {
        	'label_name': 'label',
        	'label_window': '1y',
        	'end_time': as_of_date,
        }
        test_matrix_uuid = metta.archive_matrix(test_metadata, test_matrix, format='csv')
        
        # The MettaCSVMatrixStore bundles the matrix and metadata together
        # for catwalk to use
        test_matrix_store = MettaCSVMatrixStore(
        	matrix_path='{}.csv'.format(test_matrix_uuid),
        	metadata_path='{}.yaml'.format(test_matrix_uuid)
        )
        
        # The ModelStorageEngine handles the persistence of model pickles
        # In this case, we are using FSModelStorageEngine to use the local filesystem
        model_storage_engine = FSModelStorageEngine(project_path)
        
        # To ensure that we can relate all of our persistent database records with
        # each other, we bind them together with an experiment hash. This is based
        # on the hash of experiment configuration that you pass in here, so if the
        # code fails halfway through and has to run a second time, it will use the
        # already-trained models but save the new ones under the same experment
        # hash.
        
        # Here, we will just save a trivial experiment configuration.
        # You can put any information you want in here, as long as it is hashable
        experiment_hash = save_experiment_and_get_hash({'name': 'myexperimentname'}, db_engine)
        
        # instantiate pipeline objects. these will to the brunt of the work
        trainer = ModelTrainer(
        	project_path=project_path,
        	experiment_hash=experiment_hash,
        	model_storage_engine=model_storage_engine,
        	db_engine=db_engine,
        	model_group_keys=['label_name', 'label_window']
        )
        predictor = Predictor(
        	project_path,
        	model_storage_engine,
        	db_engine
        )
        model_evaluator = ModelEvaluator(
        	[{'metrics': ['precision@'], 'thresholds': {'top_n': [5]}}],
        	db_engine
        )
        
        # run the pipeline
        grid_config = {
        	'sklearn.linear_model.LogisticRegression': {
        		'C': [0.00001, 0.0001],
        		'penalty': ['l1', 'l2'],
        		'random_state': [2193]
        	}
        }
        
        # trainer.train_models will run the entire specified grid
        # and return database ids for each model
        model_ids = trainer.train_models(
        	grid_config=grid_config,
        	misc_db_parameters=dict(test=True),
        	matrix_store=train_matrix_store
        )
        
        for model_id in model_ids:
        	predictions_proba = predictor.predict(
        		model_id=model_id,
        		matrix_store=test_matrix_store,
        		misc_db_parameters=dict(),
        		train_matrix_columns=['feature_one', 'feature_two']
        	)
        
        	model_evaluator.evaluate(
        		predictions_proba=predictions_proba,
        		labels=test_store.labels(),
        		model_id=model_id,
        		evaluation_start_time=as_of_date,
        		evaluation_end_time=as_of_date,
        		example_frequency='6month'
        	)
        
        ```
        After running the above code, results will be stored in your Postgres database in [this structure](https://github.com/dssg/results-schema/blob/master/results_schema/schema.py)
        
        In addition to being usable on the design matrices of your current project, Catwalk's functionality is used in [triage](https://github.com/dssg/triage) as a part of an entire modeling experiment that incorporates earlier tasks like feature generation and matrix building.
        
Platform: UNKNOWN
Classifier: Development Status :: 2 - Pre-Alpha
Classifier: Intended Audience :: Developers
Classifier: Natural Language :: English
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
