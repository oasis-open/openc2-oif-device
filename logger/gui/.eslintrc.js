module.exports = {
  extends: [
    'airbnb',
    'airbnb-typescript',
    'airbnb/hooks',
    'plugin:@typescript-eslint/recommended',
    'plugin:jest/recommended',
    'plugin:promise/recommended',
    'plugin:compat/recommended',
    'plugin:prettier/recommended',
    // 'plugin:react/recommended',
    // 'plugin:import/typescript',
    // 'plugin:react-hooks/recommended',
    // 'prettier/@typescript-eslint',
    // 'prettier/react'
  ],
  env: {
    browser: true,
    node: true
  },
  globals: {
    JSX: true,
    React: true
  },
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    project: 'tsconfig.json',
    tsconfigRootDir: __dirname,
    createDefaultProgram: true
  },
  rules: {
    /*
     * 'off' or 0 - turn the rule off
     * 'warn' or 1 - turn the rule on as a warning (doesn't affect exit code)
     * 'error' or 2 - turn the rule on as an error (exit code is 1 when triggered)
     */
    // eslint-disable-next-line global-require
    ...require('./config/eslint_rules'),
    'import/extensions': 0
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: require.resolve('./config/webpack.config.eslint.js')
      }
    }
  }
};
