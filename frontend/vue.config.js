const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        port: 50001,
        allowedHosts:
            "all"
    }
    ,
})
