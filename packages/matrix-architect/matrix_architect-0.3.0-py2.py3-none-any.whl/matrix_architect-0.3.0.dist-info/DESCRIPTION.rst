Copyright ©2017,.  The University of Chicago (“Chicago”). All Rights Reserved.  

Permission to use, copy, modify, and distribute this software, including all object code and source code, and any accompanying documentation (together the “Program”) for educational and not-for-profit research purposes, without fee and without a signed licensing agreement, is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies, modifications, and distributions. For the avoidance of doubt, educational and not-for-profit research purposes excludes any service or part of selling a service that uses the Program. To obtain a commercial license for the Program, contact the Technology Commercialization and Licensing, Polsky Center for Entrepreneurship and Innovation, University of Chicago, 1452 East 53rd Street, 2nd floor, Chicago, IL 60615.

Created by Data Science and Public Policy, University of Chicago

The Program is copyrighted by Chicago. The Program is supplied "as is", without any accompanying services from Chicago. Chicago does not warrant that the operation of the Program will be uninterrupted or error-free. The end-user understands that the Program was developed for research purposes and is advised not to rely exclusively on the Program for any reason.

IN NO EVENT SHALL CHICAGO BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THE PROGRAM, EVEN IF CHICAGO HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. CHICAGO SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE PROGRAM PROVIDED HEREUNDER IS PROVIDED "AS IS". CHICAGO HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

Description: # The Architect 
        
        Plan, design, and build train and test matrices
        
        [![Build Status](https://travis-ci.org/dssg/architect.svg?branch=master)](https://travis-ci.org/dssg/architect)
        [![codecov](https://codecov.io/gh/dssg/architect/branch/master/graph/badge.svg)](https://codecov.io/gh/dssg/architect)
        [![codeclimate](https://codeclimate.com/github/dssg/architect.png)](https://codeclimate.com/github/dssg/architect)
        
        In order to run classification algorithms on source data, this data must be properly organized into design matrices. Converting cleaned data into these matrices is not a trivial task; the process of creating the needed features and labels for an experiment from source data can be complicated, creating the matrices themselves out of features and labels can be inefficient, and there is opportunity at each step to leak data backwards in time to give model trained on a matrix an unfair advantage.
        
        The Architect addresses these issues with functionality aimed at all tasks between cleaned source data (in a PostgreSQL database) and design matrices.
        
        ## Components
        
        - [LabelGenerator](architect/label_generators.py): Create binary labels suitable for a design matrix by querying a database table containing outcome events.
        - [FeatureGenerator](architect/feature_generators.py): Create aggregate features suitable for a design matrix from a set of database tables containing events. Uses [collate](https://github.com/dssg/collate/) to build aggregation SQL queries.
        - [FeatureGroupCreator](architect/feature_group_creator.py), [FeatureGroupMixer](architect/feature_group_mixer.py): Create groupings of features, and mix them using different strategies (like 'leave one out') to test their effectiveness.
        - [Planner](architect/planner.py), [Builder](architect/builders.py): Build all design matrices needed for an experiment, taking into account different labels, state configurations, and feature groups.
        
        In addition to being usable individually to assist in different aspects of building matrices in your project, the Architect components are integrated in [triage](https://github.com/dssg/triage) as a part of an entire modeling experiment that incorporates later tasks like model training and testing.
        
Platform: UNKNOWN
Classifier: Development Status :: 2 - Pre-Alpha
Classifier: Intended Audience :: Developers
Classifier: Natural Language :: English
Classifier: Programming Language :: Python :: 3.4
