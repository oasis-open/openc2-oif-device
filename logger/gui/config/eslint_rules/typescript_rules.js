// typescript Rules
module.exports = {
  '@typescript-eslint/adjacent-overload-signatures': 2,
  '@typescript-eslint/ban-ts-comment': 2,
  '@typescript-eslint/ban-types': 2,
  '@typescript-eslint/brace-style': [0, '1tbs', {
    allowSingleLine: true
  }],
  '@typescript-eslint/comma-dangle': [0, {
    arrays: 'always-multiline',
    enums: 'always-multiline',
    exports: 'always-multiline',
    functions: 'always-multiline',
    generics: 'always-multiline',
    imports: 'always-multiline',
    objects: 'always-multiline',
    tuples: 'always-multiline'
  }],
  '@typescript-eslint/comma-spacing': [0, {
    after: true,
    before: false
  }],
  '@typescript-eslint/dot-notation': [2, {
    allowIndexSignaturePropertyAccess: false,
    allowKeywords: true,
    allowPattern: '',
    allowPrivateClassPropertyAccess: false,
    allowProtectedClassPropertyAccess: false
  }],
  '@typescript-eslint/explicit-function-return-type': 0,
  '@typescript-eslint/explicit-module-boundary-types': 0,
  '@typescript-eslint/func-call-spacing': [0, 'never'],
  '@typescript-eslint/indent': [0, 2, {
    ArrayExpression: 1,
    CallExpression: {
      arguments: 1
    },
    FunctionDeclaration: {
      body: 1,
      parameters: 1
    },
    FunctionExpression: {
      body: 1,
      parameters: 1
    },
    ImportDeclaration: 1,
    ObjectExpression: 1,
    SwitchCase: 1,
    VariableDeclarator: 1,
    flatTernaryExpressions: false,
    ignoreComments: false,
    ignoredNodes: [
      'JSXElement',
      'JSXElement > *',
      'JSXAttribute',
      'JSXIdentifier',
      'JSXNamespacedName',
      'JSXMemberExpression',
      'JSXSpreadAttribute',
      'JSXExpressionContainer',
      'JSXOpeningElement',
      'JSXClosingElement',
      'JSXFragment',
      'JSXOpeningFragment',
      'JSXClosingFragment',
      'JSXText',
      'JSXEmptyExpression',
      'JSXSpreadChild'
    ],
    offsetTernaryExpressions: false,
    outerIIFEBody: 1
  }],
  '@typescript-eslint/keyword-spacing': [0, {
    after: true,
    before: true,
    overrides: {
      case: {
        after: true
      },
      return: {
        after: true
      },
      throw: {
        after: true
      }
    }
  }],
  '@typescript-eslint/lines-between-class-members': [2, 'always', {
    exceptAfterSingleLine: true
  }],
  '@typescript-eslint/member-delimiter-style': 0,
  '@typescript-eslint/naming-convention': [2,
    {
      format: ['PascalCase', 'UPPER_CASE', 'camelCase'],
      selector: 'variable'
    },
    {
      format: ['PascalCase', 'camelCase'],
      selector: 'function'
    },
    {
      format: ['PascalCase'],
      selector: 'typeLike'
    }
  ],
  '@typescript-eslint/no-array-constructor': 2,
  '@typescript-eslint/no-dupe-class-members': 2,
  '@typescript-eslint/no-empty-function': [2, {
    allow: ['arrowFunctions', 'functions', 'methods']
  }],
  '@typescript-eslint/no-empty-interface': 2,
  '@typescript-eslint/no-explicit-any': 1,
  '@typescript-eslint/no-extra-non-null-assertion': 2,
  '@typescript-eslint/no-extra-parens': [0, 'all', {
    conditionalAssign: true,
    enforceForArrowConditionals: false,
    ignoreJSX: 'all',
    nestedBinaryExpressions: false,
    returnAssign: false
  }],
  '@typescript-eslint/no-extra-semi': 0,
  '@typescript-eslint/no-implied-eval': 2,
  '@typescript-eslint/no-inferrable-types': 2,
  '@typescript-eslint/no-loop-func': 2,
  '@typescript-eslint/no-loss-of-precision': 2,
  '@typescript-eslint/no-magic-numbers': [0, {
    detectObjects: false,
    enforceConst: true,
    ignore: [],
    ignoreArrayIndexes: true
  }],
  '@typescript-eslint/no-misused-new': 2,
  '@typescript-eslint/no-namespace': 2,
  '@typescript-eslint/no-non-null-asserted-optional-chain': 2,
  '@typescript-eslint/no-non-null-assertion': 1,
  '@typescript-eslint/no-redeclare': 2,
  '@typescript-eslint/no-shadow': 2,
  '@typescript-eslint/no-this-alias': 2,
  '@typescript-eslint/no-throw-literal': 2,
  '@typescript-eslint/no-unnecessary-type-constraint': 2,
  '@typescript-eslint/no-unused-expressions': [2, {
    allowShortCircuit: false,
    allowTaggedTemplates: false,
    allowTernary: false,
    enforceForJSX: false
  }],
  '@typescript-eslint/no-unused-vars': [1, {
    args: 'after-used',
    ignoreRestSiblings: true,
    vars: 'all'
  }],
  '@typescript-eslint/no-use-before-define': [2, {
    classes: true,
    functions: true,
    variables: true
  }],
  '@typescript-eslint/no-useless-constructor': 2,
  '@typescript-eslint/no-var-requires': 0,
  '@typescript-eslint/object-curly-spacing': [0, 'always'],
  '@typescript-eslint/prefer-as-const': 2,
  '@typescript-eslint/prefer-namespace-keyword': 2,
  '@typescript-eslint/quotes': [0, 'single', {
    avoidEscape: true
  }],
  '@typescript-eslint/require-await': 0,
  '@typescript-eslint/return-await': 2,
  '@typescript-eslint/semi': [0, 'always'],
  '@typescript-eslint/space-before-function-paren': [0, {
    anonymous: 'always',
    asyncArrow: 'always',
    named: 'never'
  }],
  '@typescript-eslint/space-infix-ops': 0,
  '@typescript-eslint/triple-slash-reference': 2,
  '@typescript-eslint/type-annotation-spacing': 0
};
