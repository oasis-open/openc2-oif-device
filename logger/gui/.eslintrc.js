module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true
  },
  parserOptions: {
    allowImportExportEverywhere: true,
    ecmaFeatures: {
      generators: false,
      jsx: true,
      objectLiteralDuplicateProperties: false
    },
    ecmaVersion: 2018,
    sourceType: 'module'
  },
  plugins: [
    'compat',
    'flowtype',
    'import',
    'jsx-a11y',
    'prettier',
    'promise',
    'react'
  ],
  settings: {
    'import/resolver': {
      webpack: {
        config: require('./config/config.eslint')
      }
    }
  },
  rules: {
    ...require('./config/eslint_rules')
    // 'semi': [2, 'always']
  }
}
