# LSHEngine 
<h3>All in One for Locality-Sensitive Hashing</h3>

This repo aims to implement an engine for Locality-Sensitive Hashing (LSH). Modules should be able to be attached to this engine in order to create specific recommendations as output from the Engine.

#### The LSHEngine needs the following Packages to work properly
| Dependecies | Why we need that          | Version |
| :---:       |    :----:                 |  :---:  |
| regex       | Find paterns              | NaN     |
| pandas      | Dataframe integration     | NaN     |
| numpy       | Multi Dimensional Arrays  | NaN     |
<hr/>

#### The Engine consists of two main components

<h5>A Database</h5>
The database is used to bring the values into a standardised format and to combine several data sources in order to achieve modularity.

<h5>A Model Manager</h5>

The model manager has the task of logging the values stored in the database and setting them in such a way that locality-sensitive hashing can subsequently be performed on the database.
<hr/>

#### Use in production

When you are satisfied with your model, you can save it via the engine and a binary file will be created using the Huffmann codec. This means the File will only have half the size of your regular Model. 

You can later upload the model again without re-integrating all external data sources 
<hr>

#### Usage cases

<h5>Create Database from CSV File</h5>
    
    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Create a Database with help of the Database Manager Instance from a CSV File
    DB.create_db(["example.csv"])
    
<h5>Create Database from CSV String</h5>

    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Create a Database with help of the Database Manager Instance from a CSV String
    DB.create_db("ID,Name\n0,ABC\n1,CBA\n2,CNN")
    
 <h5>Init Database</h5>
    
    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Init a Database with help of the Database Manager Instance
    DB.init_db()
    
<h5>Append new Modules to the Database</h5>

    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Init a Database with help of the Database Manager Instance
    DB.init_db()
    #Append a new Module to an existing Database
    DB.append_modules_to_db(["example.csv"])
    
<h5>Define Scope in which LSH will be executed</h5>

    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Create a Database with help of the Database Manager Instance from a CSV File
    DB.create_db(["example.csv"])
    #Set Scope
    DB.define_scope(["ID", "Name"])

<h5>Passing Database to Engine</h5>

    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Create a Database with help of the Database Manager Instance from a CSV File
    DB.create_db(["example.csv"])
    #Set Scope
    DB.define_scope(["ID", "Name"])
    #Import Engine Class
    from LSHEngine import LSHEngine
    #Create an instance of the Engine Class
    EngineInstance = LSHEngine.Engine()
    #Start Engine
    EngineInstance.GO()
    #Set the current Database the Engine should use
    EngineInstance.include_custom_manager(DB)

<h5>Performing LSH with Engine</h5>

    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Create a Database with help of the Database Manager Instance from a CSV File
    DB.create_db(["example.csv"])
    #Set Scope
    DB.define_scope(["ID", "Name"])
    #Import Engine Class
    from LSHEngine import LSHEngine
    #Create an instance of the Engine Class
    EngineInstance = LSHEngine.Engine()
    #Start Engine
    EngineInstance.GO()
    #Set the current Database the Engine should use
    EngineInstance.include_custom_manager(DB)
    #Create Forest from Database
    EngineInstance.train_forest()
    #Get Recommendations to a Search Term
    rec = EngineInstance.recommendations("1 ABC")

<h5>Save Database from ModelManager to .bin File</h5>

    #Import Database Manager
    from LSHEngine.ModelManager import LSHClientDB
    #Create an instance of the Database Manager Object
    DB = LSHClientDB.Manager()
    #Create a Database with help of the Database Manager Instance from a CSV File
    DB.create_db(["example.csv"])
    #Set Scope
    DB.define_scope(["ID", "Name"])
    #Import Engine Class
    from LSHEngine import LSHEngine
    #Create an instance of the Engine Class
    EngineInstance = LSHEngine.Engine()
    #Start Engine
    EngineInstance.GO()
    #Set the current Database the Engine should use
    EngineInstance.include_custom_manager(DB)
    #Save DB to .bin File
    EngineInstance.save_model_to_bin("example.bin")

<h5>Load Database from .bin File</h5>

    #Import Engine Class
    from LSHEngine import LSHEngine
    #Create an instance of the Engine Class
    EngineInstance = LSHEngine.Engine()
    #Start Engine
    EngineInstance.GO()
    #Load Database into Engine
    EngineInstance.load("example.bin")