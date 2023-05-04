const { defineConfig } = require('cypress')

module.exports = defineConfig({
  projectId: 'v3xf2m',
  e2e: {
    baseUrl: 'http://r78-test.zdrav.netrika.ru/tm.doctorportal.ui/',
  },
})

