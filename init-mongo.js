db.createUser({
    user: "testuser",
    pwd: "testpassword",
    roles: [{
        role:"readWrite",
        db: "IReNEdb"
    }]
});

db.collaborators.insertOne({
    "first_name": "Pepe",
    "last_name": "Figueroa",
    "email": "pepe.figueroa@upr.edu",
    "banned": false,
    "approved": true
})
