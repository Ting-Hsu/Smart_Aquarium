const { Sequelize, DataTypes } = require('sequelize');
const db = new Sequelize('aiot082021', 'aiot082021', '0bURRTg7O6x5lZ72', {
    host: 'ppppp196.synology.me',
    dialect: 'mysql',
    port: 33306,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
})

const Model = {
    member : db.define('member', {
        id: {
            type: Sequelize.DataTypes.INTEGER,
            autoIncrement: true,
            primaryKey: true,
        },
        username:{
            type: Sequelize.DataTypes.STRING,
            allowNull: false,
        },
        password:{
            type: Sequelize.DataTypes.STRING,
            allowNull: false,
        },
        email:{
            type: Sequelize.DataTypes.STRING,
            allowNull: true
        },
        createdDate:{
            type: Sequelize.DataTypes.DATE,
            allowNull:false
        } 
    }),
    Temp : db.define('temp', {
        id: {
            type: Sequelize.DataTypes.INTEGER,
            autoIncrement: true,
            primaryKey: true,
        },
        temp : {
            type: Sequelize.DataTypes.FLOAT,
            allowNull: true,
        },
        createdDate : {
            type: Sequelize.DataTypes.DATE,
        }
    }),
    File : db.define('file', {
        id: {
            type: Sequelize.DataTypes.INTEGER,
            autoIncrement: true,
            primaryKey: true,
        },
        file : {
            type: Sequelize.DataTypes.BLOB("long"),
            allowNull: true,
        },
        createdDate : {
            type: Sequelize.DataTypes.DATE
        } 
    })
}
// Model.member.sync({force: false})
// Model.Temp.sync({force: false})
// Model.File.sync({force: false})

console.log("MySQL資料庫初始化設定完成 ! ! ")

module.exports = Model;
