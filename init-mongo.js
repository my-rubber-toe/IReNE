/**
 * Database Configuration File
 * 
 * Author: Roberto Y. Guzman - roberto.guzman3@upr.edu
 * 
 * The service container "irene-db" of the docker-compose.yml file requires this configuration file to 
 * sets up the database username, user password, user role and database name to be used.
 * 
 * The connection string for the database system will be:
 * 
 * mongodb://<databaseUser>:<databasePassword>@irene-db:27017/?authSource=admin 
 * 
 */

const databaseUser = "testuser";
const databasePassword = "testpassword";
const userRole = "readWrite";
const databaseToUse = "IReNEdb";

db.createUser({
  user: databaseUser,
  pwd: databasePassword,
  roles: [{
      role: userRole,
      db: databaseToUse
  }]
});
