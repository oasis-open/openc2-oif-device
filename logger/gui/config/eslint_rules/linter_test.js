yarn run v1.21.1
$ /Users/jerome.czachor/Documents/git/Screaming_Bunny/Schema/electron_app/node_modules/.bin/eslint --print-config babel.config.js
{
  "env": {
    "browser": true,
    "node": true,
    "es6": true
  },
  "globals": {},
  "parser": "/Users/jerome.czachor/Documents/git/Screaming_Bunny/Schema/electron_app/node_modules/babel-eslint/lib/index.js",
  "parserOptions": {
    "allowImportExportEverywhere": true,
    "ecmaFeatures": {
      "jsx": true,
      "generators": false,
      "objectLiteralDuplicateProperties": false
    },
    "ecmaVersion": 2018,
    "sourceType": "module"

  },
  "plugins": [
    "jsx-a11y",
    "prettier",
    "react",
    "compat",
    "promise",
    "import",
    "flowtype"
  ],
  "settings": {
    "import/resolver": {
      "webpack": {
        "config": "/Users/jerome.czachor/Documents/git/Screaming_Bunny/Schema/electron_app/config/webpack.config.eslint.js"
      },
      "node": {
        "extensions": [
          ".js",
          ".jsx",
          ".json"
        ]
      }
    },
    "react": {
      "pragma": "React",
      "version": "detect"
    },
    "propWrapperFunctions": [
      "forbidExtraProps",
      "exact",
      "Object.freeze"
    ],
    "import/extensions": [
      ".js",
      ".mjs",
      ".jsx"
    ],
    "import/core-modules": [],
    "import/ignore": [
      "node_modules",
      "\\.(coffee|scss|css|less|hbs|svg|json)$"
    ]
  },
  "rules": {
    "accessor-pairs": [
      0
    ],
    "array-bracket-newline": [
      0,
      "consistent"
    ],
    "array-bracket-spacing": [
      0,
      "never"
    ],
    "array-callback-return": [
      2,
      {
        "allowImplicit": true
      }
    ],
    "array-element-newline": [
      0,
      {
        "multiline": true,
        "minItems": 3
      }
    ],
    "arrow-body-style": [
      0,
      "as-needed",
      {
        "requireReturnForObjectLiteral": false
      }
    ],
    "arrow-parens": [
      0,
      "always"
    ],
    "arrow-spacing": [
      0,
      {
        "after": true,
        "before": true
      }
    ],
    "block-scoped-var": [
      2
    ],
    "block-spacing": [
      0,
      "always"
    ],
    "brace-style": [
      0,
      "1tbs",
      {
        "allowSingleLine": true
      }
    ],
    "callback-return": [
      0
    ],
    "camelcase": [
      1,
      {
        "ignoreDestructuring": true,
        "ignoreImports": true,
        "properties": "never"
      }
    ],
    "capitalized-comments": [
      0,
      "never",
      {
        "line": {
          "ignoreConsecutiveComments": true,
          "ignoreInlineComments": true,
          "ignorePattern": ".*"
        },
        "block": {
          "ignoreConsecutiveComments": true,
          "ignoreInlineComments": true,
          "ignorePattern": ".*"
        }
      }
    ],
    "class-methods-use-this": [
      2,
      {
        "exceptMethods": [
          "render",
          "getInitialState",
          "getDefaultProps",
          "getChildContext",
          "componentWillMount",
          "UNSAFE_componentWillMount",
          "componentDidMount",
          "componentWillReceiveProps",
          "UNSAFE_componentWillReceiveProps",
          "shouldComponentUpdate",
          "componentWillUpdate",
          "UNSAFE_componentWillUpdate",
          "componentDidUpdate",
          "componentWillUnmount",
          "componentDidCatch",
          "getSnapshotBeforeUpdate"
        ]
      }
    ],
    "comma-dangle": [
      2,
      "never"
    ],
    "comma-spacing": [
      2,
      {
        "after": true,
        "before": false
      }
    ],
    "comma-style": [
      2,
      "last",
      {
        "exceptions": {
          "ArrayExpression": false,
          "ArrowFunctionExpression": false,
          "ArrayPattern": false,
          "CallExpression": false,
          "FunctionDeclaration": false,
          "FunctionExpression": false,
          "ImportDeclaration": false,
          "ObjectExpression": false,
          "ObjectPattern": false,
          "VariableDeclaration": false,
          "NewExpression": false
        }
      }
    ],
    "complexity": [
      0,
      11
    ],
    "computed-property-spacing": [
      0,
      "never"
    ],
    "consistent-return": [
      0
    ],
    "consistent-this": [
      0
    ],
    "constructor-super": [
      2
    ],
    "curly": [
      2,
      "multi-line"
    ],
    "default-case": [
      2,
      {
        "commentPattern": "^no default$"
      }
    ],
    "dot-location": [
      0,
      "property"
    ],
    "dot-notation": [
      2,
      {
        "allowKeywords": true,
        "allowPattern": ""
      }
    ],
    "eol-last": [
      0,
      "always"
    ],
    "eqeqeq": [
      2,
      "always",
      {
        "null": "ignore"
      }
    ],
    "for-direction": [
      2
    ],
    "func-call-spacing": [
      0,
      "never"
    ],
    "func-name-matching": [
      0,
      "always",
      {
        "considerPropertyDescriptor": true,
        "includeCommonJSModuleExports": false
      }
    ],
    "func-names": [
      1
    ],
    "func-style": [
      0,
      "expression"
    ],
    "function-call-argument-newline": [
      0
    ],
    "function-paren-newline": [
      0,
      "consistent"
    ],
    "generator-star": [
      0
    ],
    "generator-star-spacing": [
      0,
      {
        "after": true,
        "before": false
      }
    ],
    "getter-return": [
      2,
      {
        "allowImplicit": true
      }
    ],
    "global-require": [
      2
    ],
    "guard-for-in": [
      2
    ],
    "handle-callback-err": [
      0
    ],
    "id-blacklist": [
      0
    ],
    "id-length": [
      0
    ],
    "id-match": [
      0
    ],
    "implicit-arrow-linebreak": [
      2,
      "beside"
    ],
    "indent": [
      0,
      2,
      {
        "ignoreComments": false,
        "ignoredNodes": [
          "JSXElement",
          "JSXElement > *",
          "JSXAttribute",
          "JSXIdentifier",
          "JSXNamespacedName",
          "JSXMemberExpression",
          "JSXSpreadAttribute",
          "JSXExpressionContainer",
          "JSXOpeningElement",
          "JSXClosingElement",
          "JSXText",
          "JSXEmptyExpression",
          "JSXSpreadChild"
        ],
        "flatTernaryExpressions": false,
        "outerIIFEBody": 1,
        "ArrayExpression": 1,
        "CallExpression": {
          "arguments": 1
        },
        "FunctionDeclaration": {
          "parameters": 1,
          "body": 1
        },
        "FunctionExpression": {
          "parameters": 1,
          "body": 1
        },
        "ImportDeclaration": 1,
        "ObjectExpression": 1,
        "SwitchCase": 1,
        "VariableDeclarator": 1
      }
    ],
    "indent-legacy": [
      0
    ],
    "init-declarations": [
      0
    ],
    "jsx-quotes": [
      0,
      "prefer-double"
    ],
    "key-spacing": [
      0,
      {
        "beforeColon": false,
        "afterColon": true
      }
    ],
    "keyword-spacing": [
      2,
      {
        "after": true,
        "before": true,
        "overrides": {
          "case": {
            "after": true
          },
          "return": {
            "after": true
          },
          "throw": {
            "after": true
          }
        }
      }
    ],
    "line-comment-position": [
      0,
      {
        "applyDefaultPatterns": true,
        "ignorePattern": "",
        "position": "above"
      }
    ],
    "linebreak-style": [
      0,
      "unix"
    ],
    "lines-around-comment": [
      0
    ],
    "lines-around-directive": [
      2,
      {
        "after": "always",
        "before": "always"
      }
    ],
    "lines-between-class-members": [
      2,
      "always",
      {
        "exceptAfterSingleLine": false
      }
    ],
    "max-classes-per-file": [
      2,
      1
    ],
    "max-depth": [
      0,
      4
    ],
    "max-len": [
      1,
      120,
      2,
      {
        "ignoreComments": true,
        "ignoreRegExpLiterals": true,
        "ignoreStrings": true,
        "ignoreTemplateLiterals": true,
        "ignoreUrls": true
      }
    ],
    "max-lines": [
      0,
      {
        "max": 300,
        "skipBlankLines": true,
        "skipComments": true
      }
    ],
    "max-lines-per-function": [
      0,
      {
        "max": 50,
        "skipBlankLines": true,
        "skipComments": true,
        "IIFEs": true
      }
    ],
    "max-nested-callbacks": [
      0
    ],
    "max-params": [
      0,
      3
    ],
    "max-statements": [
      0,
      10
    ],
    "max-statements-per-line": [
      0,
      {
        "max": 1
      }
    ],
    "multiline-comment-style": [
      0,
      "starred-block"
    ],
    "multiline-ternary": [
      1,
      "never"
    ],
    "new-cap": [
      2,
      {
        "newIsCap": true,
        "newIsCapExceptions": [],
        "capIsNew": false,
        "capIsNewExceptions": [
          "Immutable.Map",
          "Immutable.Set",
          "Immutable.List"
        ],
        "properties": true
      }
    ],
    "new-parens": [
      0
    ],
    "newline-after-var": [
      0
    ],
    "newline-before-return": [
      0
    ],
    "newline-per-chained-call": [
      0,
      {
        "ignoreChainWithDepth": 4
      }
    ],
    "no-alert": [
      1
    ],
    "no-array-constructor": [
      2
    ],
    "no-arrow-condition": [
      0
    ],
    "no-async-promise-executor": [
      2
    ],
    "no-await-in-loop": [
      2
    ],
    "no-bitwise": [
      2
    ],
    "no-buffer-constructor": [
      2
    ],
    "no-caller": [
      2
    ],
    "no-case-declarations": [
      0
    ],
    "no-catch-shadow": [
      0
    ],
    "no-class-assign": [
      2
    ],
    "no-comma-dangle": [
      0
    ],
    "no-compare-neg-zero": [
      2
    ],
    "no-cond-assign": [
      2,
      "always"
    ],
    "no-confusing-arrow": [
      0,
      {
        "allowParens": true
      }
    ],
    "no-console": [
      0
    ],
    "no-const-assign": [
      2
    ],
    "no-constant-condition": [
      1
    ],
    "no-continue": [
      2
    ],
    "no-control-regex": [
      2
    ],
    "no-debugger": [
      2
    ],
    "no-delete-var": [
      2
    ],
    "no-div-regex": [
      0
    ],
    "no-dupe-args": [
      2
    ],
    "no-dupe-class-members": [
      2
    ],
    "no-dupe-keys": [
      2
    ],
    "no-duplicate-case": [
      2
    ],
    "no-duplicate-imports": [
      0
    ],
    "no-else-return": [
      2,
      {
        "allowElseIf": false
      }
    ],
    "no-empty": [
      2
    ],
    "no-empty-character-class": [
      2
    ],
    "no-empty-function": [
      2,
      {
        "allow": [
          "arrowFunctions",
          "functions",
          "methods"
        ]
      }
    ],
    "no-empty-pattern": [
      2
    ],
    "no-eq-null": [
      0
    ],
    "no-eval": [
      2
    ],
    "no-ex-assign": [
      2
    ],
    "no-extend-native": [
      2
    ],
    "no-extra-bind": [
      2
    ],
    "no-extra-boolean-cast": [
      2
    ],
    "no-extra-label": [
      2
    ],
    "no-extra-parens": [
      0,
      "all",
      {
        "conditionalAssign": true,
        "enforceForArrowConditionals": false,
        "ignoreJSX": "all",
        "nestedBinaryExpressions": false,
        "returnAssign": false
      }
    ],
    "no-extra-semi": [
      0
    ],
    "no-fallthrough": [
      0
    ],
    "no-floating-decimal": [
      0
    ],
    "no-func-assign": [
      2
    ],
    "no-global-assign": [
      2,
      {
        "exceptions": []
      }
    ],
    "no-implicit-coercion": [
      0,
      {
        "allow": [],
        "boolean": false,
        "number": true,
        "string": true
      }
    ],
    "no-implicit-globals": [
      0
    ],
    "no-implied-eval": [
      2
    ],
    "no-inline-comments": [
      0
    ],
    "no-inner-declarations": [
      2
    ],
    "no-invalid-regexp": [
      2
    ],
    "no-invalid-this": [
      0
    ],
    "no-irregular-whitespace": [
      2
    ],
    "no-iterator": [
      2
    ],
    "no-label-var": [
      2
    ],
    "no-labels": [
      2,
      {
        "allowLoop": false,
        "allowSwitch": false
      }
    ],
    "no-lone-blocks": [
      2
    ],
    "no-lonely-if": [
      2
    ],
    "no-loop-func": [
      2
    ],
    "no-magic-numbers": [
      0,
      {
        "detectObjects": false,
        "enforceConst": true,
        "ignore": [],
        "ignoreArrayIndexes": true
      }
    ],
    "no-misleading-character-class": [
      2
    ],
    "no-mixed-operators": [
      0,
      {
        "groups": [
          [
            "%",
            "**"
          ],
          [
            "%",
            "+"
          ],
          [
            "%",
            "-"
          ],
          [
            "%",
            "*"
          ],
          [
            "%",
            "/"
          ],
          [
            "/",
            "*"
          ],
          [
            "&",
            "|",
            "<<",
            ">>",
            ">>>"
          ],
          [
            "==",
            "!=",
            "===",
            "!=="
          ],
          [
            "&&",
            "||"
          ]
        ],
        "allowSamePrecedence": false
      }
    ],
    "no-mixed-requires": [
      0,
      false
    ],
    "no-mixed-spaces-and-tabs": [
      0
    ],
    "no-multi-assign": [
      0
    ],
    "no-multi-spaces": [
      0,
      {
        "ignoreEOLComments": false
      }
    ],
    "no-multi-str": [
      2
    ],
    "no-multiple-empty-lines": [
      2,
      {
        "max": 2,
        "maxBOF": 1,
        "maxEOF": 0
      }
    ],
    "no-native-reassign": [
      0
    ],
    "no-negated-condition": [
      0
    ],
    "no-negated-in-lhs": [
      0
    ],
    "no-nested-ternary": [
      2
    ],
    "no-new": [
      2
    ],
    "no-new-func": [
      2
    ],
    "no-new-object": [
      2
    ],
    "no-new-require": [
      2
    ],
    "no-new-symbol": [
      2
    ],
    "no-new-wrappers": [
      2
    ],
    "no-obj-calls": [
      2
    ],
    "no-octal": [
      2
    ],
    "no-octal-escape": [
      2
    ],
    "no-param-reassign": [
      1,
      {
        "props": true,
        "ignorePropertyModificationsFor": [
          "acc",
          "accumulator",
          "e",
          "ctx",
          "req",
          "request",
          "res",
          "response",
          "$scope",
          "staticContext"
        ]
      }
    ],
    "no-path-concat": [
      2
    ],
    "no-plusplus": [
      2,
      {
        "allowForLoopAfterthoughts": true
      }
    ],
    "no-process-env": [
      0
    ],
    "no-process-exit": [
      0
    ],
    "no-proto": [
      2
    ],
    "no-prototype-builtins": [
      2
    ],
    "no-redeclare": [
      2
    ],
    "no-regex-spaces": [
      2
    ],
    "no-reserved-keys": [
      0
    ],
    "no-restricted-globals": [
      2,
      "isFinite",
      "isNaN",
      "addEventListener",
      "blur",
      "close",
      "closed",
      "confirm",
      "defaultStatus",
      "defaultstatus",
      "event",
      "external",
      "find",
      "focus",
      "frameElement",
      "frames",
      "history",
      "innerHeight",
      "innerWidth",
      "length",
      "location",
      "locationbar",
      "menubar",
      "moveBy",
      "moveTo",
      "name",
      "onblur",
      "onerror",
      "onfocus",
      "onload",
      "onresize",
      "onunload",
      "open",
      "opener",
      "opera",
      "outerHeight",
      "outerWidth",
      "pageXOffset",
      "pageYOffset",
      "parent",
      "print",
      "removeEventListener",
      "resizeBy",
      "resizeTo",
      "screen",
      "screenLeft",
      "screenTop",
      "screenX",
      "screenY",
      "scroll",
      "scrollbars",
      "scrollBy",
      "scrollTo",
      "scrollX",
      "scrollY",
      "self",
      "status",
      "statusbar",
      "stop",
      "toolbar",
      "top"
    ],
    "no-restricted-imports": [
      0,
      {
        "paths": [],
        "patterns": []
      }
    ],
    "no-restricted-modules": [
      0
    ],
    "no-restricted-properties": [
      2,
      {
        "object": "arguments",
        "property": "callee",
        "message": "arguments.callee is deprecated"
      },
      {
        "object": "global",
        "property": "isFinite",
        "message": "Please use Number.isFinite instead"
      },
      {
        "object": "self",
        "property": "isFinite",
        "message": "Please use Number.isFinite instead"
      },
      {
        "object": "window",
        "property": "isFinite",
        "message": "Please use Number.isFinite instead"
      },
      {
        "object": "global",
        "property": "isNaN",
        "message": "Please use Number.isNaN instead"
      },
      {
        "object": "self",
        "property": "isNaN",
        "message": "Please use Number.isNaN instead"
      },
      {
        "object": "window",
        "property": "isNaN",
        "message": "Please use Number.isNaN instead"
      },
      {
        "property": "__defineGetter__",
        "message": "Please use Object.defineProperty instead."
      },
      {
        "property": "__defineSetter__",
        "message": "Please use Object.defineProperty instead."
      },
      {
        "object": "Math",
        "property": "pow",
        "message": "Use the exponentiation operator (**) instead."
      }
    ],
    "no-restricted-syntax": [
      2,
      {
        "selector": "ForInStatement",
        "message": "for..in loops iterate over the entire prototype chain, which is virtually never what you want. Use Object.{keys,values,entries}, and iterate over the resulting array."
      },
      {
        "selector": "ForOfStatement",
        "message": "iterators/generators require regenerator-runtime, which is too heavyweight for this guide to allow them. Separately, loops should be avoided in favor of array iterations."
      },
      {
        "selector": "LabeledStatement",
        "message": "Labels are a form of GOTO; using them makes code confusing and hard to maintain and understand."
      },
      {
        "selector": "WithStatement",
        "message": "`with` is disallowed in strict mode because it makes code impossible to predict and optimize."
      }
    ],
    "no-return-assign": [
      2,
      "always"
    ],
    "no-return-await": [
      2
    ],
    "no-script-url": [
      2
    ],
    "no-self-assign": [
      2,
      {
        "props": true
      }
    ],
    "no-self-compare": [
      2
    ],
    "no-sequences": [
      2
    ],
    "no-shadow": [
      2
    ],
    "no-shadow-restricted-names": [
      2
    ],
    "no-space-before-semi": [
      0
    ],
    "no-spaced-func": [
      2
    ],
    "no-sparse-arrays": [
      2
    ],
    "no-sync": [
      0
    ],
    "no-tabs": [
      0
    ],
    "no-template-curly-in-string": [
      2
    ],
    "no-ternary": [
      0
    ],
    "no-this-before-super": [
      2
    ],
    "no-throw-literal": [
      2
    ],
    "no-trailing-spaces": [
      2,
      {
        "ignoreComments": false,
        "skipBlankLines": false
      }
    ],
    "no-undef": [
      2
    ],
    "no-undef-init": [
      2
    ],
    "no-undefined": [
      0
    ],
    "no-underscore-dangle": [
      1,
      {
        "allow": [
          "__REDUX_DEVTOOLS_EXTENSION_COMPOSE__"
        ],
        "allowAfterSuper": false,
        "allowAfterThis": false,
        "allowAfterThisConstructor": false,
        "enforceInMethodNames": true
      }
    ],
    "no-unexpected-multiline": [
      0
    ],
    "no-unmodified-loop-condition": [
      0
    ],
    "no-unneeded-ternary": [
      2,
      {
        "defaultAssignment": false
      }
    ],
    "no-unreachable": [
      2
    ],
    "no-unsafe-finally": [
      2
    ],
    "no-unsafe-negation": [
      2
    ],
    "no-unused-expressions": [
      2,
      {
        "allowShortCircuit": false,
        "allowTaggedTemplates": false,
        "allowTernary": false
      }
    ],
    "no-unused-labels": [
      2
    ],
    "no-unused-vars": [
      2,
      {
        "args": "after-used",
        "ignoreRestSiblings": true,
        "vars": "all"
      }
    ],
    "no-use-before-define": [
      2,
      {
        "classes": true,
        "functions": true,
        "variables": true
      }
    ],
    "no-useless-call": [
      0
    ],
    "no-useless-catch": [
      2
    ],
    "no-useless-computed-key": [
      2
    ],
    "no-useless-concat": [
      2
    ],
    "no-useless-constructor": [
      2
    ],
    "no-useless-escape": [
      2
    ],
    "no-useless-rename": [
      2,
      {
        "ignoreDestructuring": false,
        "ignoreExport": false,
        "ignoreImport": false
      }
    ],
    "no-useless-return": [
      2
    ],
    "no-var": [
      2
    ],
    "no-void": [
      2
    ],
    "no-warning-comments": [
      0,
      {
        "location": "start",
        "terms": [
          "todo",
          "fixme",
          "xxx"
        ]
      }
    ],
    "no-whitespace-before-property": [
      0
    ],
    "no-with": [
      2
    ],
    "no-wrap-func": [
      0
    ],
    "nonblock-statement-body-position": [
      0,
      "beside",
      {
        "overrides": {}
      }
    ],
    "object-curly-newline": [
      2,
      {
        "ExportDeclaration": {
          "consistent": true,
          "minProperties": 4,
          "multiline": true
        },
        "ImportDeclaration": {
          "consistent": true,
          "minProperties": 4,
          "multiline": true
        }
      }
    ],
    "object-curly-spacing": [
      0,
      "always"
    ],
    "object-property-newline": [
      0,
      {
        "allowAllPropertiesOnSameLine": true,
        "allowMultiplePropertiesPerLine": false
      }
    ],
    "object-shorthand": [
      2,
      "always",
      {
        "avoidQuotes": true,
        "ignoreConstructors": false
      }
    ],
    "one-var": [
      2,
      "never"
    ],
    "one-var-declaration-per-line": [
      0,
      "always"
    ],
    "operator-assignment": [
      2,
      "always"
    ],
    "operator-linebreak": [
      2,
      "before",
      {
        "overrides": {
          "=": "none"
        }
      }
    ],
    "padded-blocks": [
      0,
      {
        "blocks": "never",
        "classes": "never",
        "switches": "never"
      },
      {
        "allowSingleLineBlocks": true
      }
    ],
    "padding-line-between-statements": [
      0
    ],
    "prefer-arrow-callback": [
      0,
      {
        "allowNamedFunctions": false,
        "allowUnboundThis": true
      }
    ],
    "prefer-const": [
      2,
      {
        "destructuring": "any",
        "ignoreReadBeforeAssign": true
      }
    ],
    "prefer-destructuring": [
      0,
      {
        "AssignmentExpression": {
          "array": true,
          "object": false
        },
        "VariableDeclarator": {
          "array": false,
          "object": true
        }
      },
      {
        "enforceForRenamedProperties": false
      }
    ],
    "prefer-named-capture-group": [
      0
    ],
    "prefer-numeric-literals": [
      2
    ],
    "prefer-object-spread": [
      2
    ],
    "prefer-promise-reject-errors": [
      2,
      {
        "allowEmptyReject": true
      }
    ],
    "prefer-reflect": [
      0
    ],
    "prefer-rest-params": [
      2
    ],
    "prefer-spread": [
      2
    ],
    "prefer-template": [
      2
    ],
    "quote-props": [
      0,
      "as-needed",
      {
        "keywords": false,
        "numbers": false,
        "unnecessary": true
      }
    ],
    "quotes": [
      2,
      "single",
      {
        "allowTemplateLiterals": true,
        "avoidEscape": true
      }
    ],
    "radix": [
      2
    ],
    "require-atomic-updates": [
      0
    ],
    "require-await": [
      0
    ],
    "require-jsdoc": [
      0
    ],
    "require-unicode-regexp": [
      0
    ],
    "require-yield": [
      2
    ],
    "rest-spread-spacing": [
      0,
      "never"
    ],
    "semi": [
      2,
      "always"
    ],
    "semi-spacing": [
      2,
      {
        "after": true,
        "before": false
      }
    ],
    "semi-style": [
      0,
      "last"
    ],
    "sort-imports": [
      0,
      {
        "ignoreCase": false,
        "ignoreDeclarationSort": false,
        "ignoreMemberSort": false,
        "memberSyntaxSortOrder": [
          "none",
          "all",
          "multiple",
          "single"
        ]
      }
    ],
    "sort-keys": [
      0,
      "asc",
      {
        "caseSensitive": false,
        "natural": true
      }
    ],
    "sort-vars": [
      0
    ],
    "space-after-function-name": [
      0
    ],
    "space-after-keywords": [
      0
    ],
    "space-before-blocks": [
      2
    ],
    "space-before-function-paren": [
      2,
      {
        "anonymous": "always",
        "asyncArrow": "always",
        "named": "never"
      }
    ],
    "space-before-function-parentheses": [
      0
    ],
    "space-before-keywords": [
      0
    ],
    "space-in-brackets": [
      0
    ],
    "space-in-parens": [
      0,
      "never"
    ],
    "space-infix-ops": [
      0
    ],
    "space-return-throw-case": [
      0
    ],
    "space-unary-ops": [
      0,
      {
        "nonwords": false,
        "overrides": {},
        "words": true
      }
    ],
    "space-unary-word-ops": [
      0
    ],
    "spaced-comment": [
      2,
      "always",
      {
        "block": {
          "balanced": true,
          "exceptions": [
            "-",
            "+"
          ],
          "markers": [
            "=",
            "!",
            ":",
            "::"
          ]
        },
        "line": {
          "exceptions": [
            "-",
            "+"
          ],
          "markers": [
            "=",
            "!"
          ]
        }
      }
    ],
    "strict": [
      2,
      "never"
    ],
    "switch-colon-spacing": [
      0,
      {
        "before": false,
        "after": true
      }
    ],
    "symbol-description": [
      2
    ],
    "template-curly-spacing": [
      0
    ],
    "template-tag-spacing": [
      0,
      "never"
    ],
    "unicode-bom": [
      0,
      "never"
    ],
    "use-isnan": [
      2
    ],
    "valid-jsdoc": [
      0
    ],
    "valid-typeof": [
      2,
      {
        "requireStringLiterals": true
      }
    ],
    "vars-on-top": [
      2
    ],
    "wrap-iife": [
      0,
      "outside",
      {
        "functionPrototypeMethods": false
      }
    ],
    "wrap-regex": [
      0
    ],
    "yield-star-spacing": [
      0,
      "after"
    ],
    "yoda": [
      2
    ],
    "compat/compat": [
      2
    ],
    "prettier/prettier": [
      0,
      {
        "parser": "flow",
        "singleQuote": true
      }
    ],
    "flowtype/boolean-style": [
      2,
      "boolean"
    ],
    "flowtype/define-flow-type": [
      1
    ],
    "flowtype/delimiter-dangle": [
      2,
      "never"
    ],
    "flowtype/generic-spacing": [
      2,
      "never"
    ],
    "flowtype/no-primitive-constructor-types": [
      2
    ],
    "flowtype/no-weak-types": [
      1
    ],
    "flowtype/object-type-delimiter": [
      2,
      "comma"
    ],
    "flowtype/require-parameter-type": [
      0
    ],
    "flowtype/require-return-type": [
      0
    ],
    "flowtype/require-valid-file-annotation": [
      0
    ],
    "flowtype/semi": [
      2,
      "always"
    ],
    "flowtype/space-after-type-colon": [
      2,
      "always"
    ],
    "flowtype/space-before-generic-bracket": [
      2,
      "never"
    ],
    "flowtype/space-before-type-colon": [
      2,
      "never"
    ],
    "flowtype/union-intersection-spacing": [
      2,
      "always"
    ],
    "flowtype/use-flow-type": [
      2
    ],
    "flowtype/valid-syntax": [
      2
    ],
    "import/default": [
      0
    ],
    "import/dynamic-import-chunkname": [
      0,
      {
        "importFunctions": [],
        "webpackChunknameFormat": "[0-9a-zA-Z-_/.]+"
      }
    ],
    "import/export": [
      2
    ],
    "import/exports-last": [
      0
    ],
    "import/extensions": [
      2,
      "ignorePackages",
      {
        "js": "never",
        "jsx": "never",
        "mjs": "never"
      }
    ],
    "import/first": [
      2
    ],
    "import/group-exports": [
      0
    ],
    "import/imports-first": [
      0
    ],
    "import/max-dependencies": [
      0,
      {
        "max": 10
      }
    ],
    "import/named": [
      2
    ],
    "import/namespace": [
      0
    ],
    "import/newline-after-import": [
      2
    ],
    "import/no-absolute-path": [
      2
    ],
    "import/no-amd": [
      2
    ],
    "import/no-anonymous-default-export": [
      0,
      {
        "allowAnonymousClass": false,
        "allowAnonymousFunction": false,
        "allowArray": false,
        "allowArrowFunction": false,
        "allowLiteral": false,
        "allowObject": false
      }
    ],
    "import/no-commonjs": [
      0
    ],
    "import/no-cycle": [
      2,
      {}
    ],
    "import/no-default-export": [
      0
    ],
    "import/no-deprecated": [
      0
    ],
    "import/no-duplicates": [
      2
    ],
    "import/no-dynamic-require": [
      2
    ],
    "import/no-extraneous-dependencies": [
      0,
      {
        "devDependencies": [
          "test/**",
          "tests/**",
          "spec/**",
          "**/__tests__/**",
          "**/__mocks__/**",
          "test.{js,jsx}",
          "test-*.{js,jsx}",
          "**/*{.,_}{test,spec}.{js,jsx}",
          "**/jest.config.js",
          "**/jest.setup.js",
          "**/vue.config.js",
          "**/webpack.config.js",
          "**/webpack.config.*.js",
          "**/rollup.config.js",
          "**/rollup.config.*.js",
          "**/gulpfile.js",
          "**/gulpfile.*.js",
          "**/Gruntfile{,.js}",
          "**/protractor.conf.js",
          "**/protractor.conf.*.js"
        ],
        "optionalDependencies": false
      }
    ],
    "import/no-internal-modules": [
      0,
      {
        "allow": []
      }
    ],
    "import/no-mutable-exports": [
      2
    ],
    "import/no-named-as-default": [
      2
    ],
    "import/no-named-as-default-member": [
      2
    ],
    "import/no-named-default": [
      2
    ],
    "import/no-named-export": [
      0
    ],
    "import/no-namespace": [
      0
    ],
    "import/no-nodejs-modules": [
      0
    ],
    "import/no-relative-parent-imports": [
      0
    ],
    "import/no-restricted-paths": [
      0
    ],
    "import/no-self-import": [
      2
    ],
    "import/no-unassigned-import": [
      0
    ],
    "import/no-unresolved": [
      2,
      {
        "caseSensitive": true,
        "commonjs": true
      }
    ],
    "import/no-unused-modules": [
      0,
      {
        "ignoreExports": [],
        "missingExports": true,
        "unusedExports": true
      }
    ],
    "import/no-useless-path-segments": [
      2
    ],
    "import/no-webpack-loader-syntax": [
      2
    ],
    "import/order": [
      2,
      {
        "groups": [
          [
            "builtin",
            "external",
            "internal"
          ]
        ]
      }
    ],
    "import/prefer-default-export": [
      0
    ],
    "import/unambiguous": [
      0
    ],
    "jsx-a11y/accessible-emoji": [
      2
    ],
    "jsx-a11y/alt-text": [
      2,
      {
        "area": [],
        "elements": [
          "img",
          "object",
          "area",
          "input[type='image']"
        ],
        "img": [],
        "input[type='image']": [],
        "object": []
      }
    ],
    "jsx-a11y/anchor-has-content": [
      2,
      {
        "components": []
      }
    ],
    "jsx-a11y/anchor-is-valid": [
      0,
      {
        "aspects": [
          "noHref",
          "invalidHref",
          "preferButton"
        ],
        "components": [
          "Link"
        ],
        "specialLink": [
          "to"
        ]
      }
    ],
    "jsx-a11y/aria-activedescendant-has-tabindex": [
      2
    ],
    "jsx-a11y/aria-props": [
      2
    ],
    "jsx-a11y/aria-proptypes": [
      2
    ],
    "jsx-a11y/aria-role": [
      2,
      {
        "ignoreNonDom": false,
        "ignoreNonDOM": false
      }
    ],
    "jsx-a11y/aria-unsupported-elements": [
      2
    ],
    "jsx-a11y/click-events-have-key-events": [
      2
    ],
    "jsx-a11y/control-has-associated-label": [
      2,
      {
        "controlComponents": [],
        "depth": 5,
        "ignoreElements": [
          "audio",
          "canvas",
          "embed",
          "input",
          "textarea",
          "tr",
          "video"
        ],
        "ignoreRoles": [
          "grid",
          "listbox",
          "menu",
          "menubar",
          "radiogroup",
          "row",
          "tablist",
          "toolbar",
          "tree",
          "treegrid"
        ],
        "labelAttributes": [
          "label"
        ]
      }
    ],
    "jsx-a11y/heading-has-content": [
      2,
      {
        "components": [
          ""
        ]
      }
    ],
    "jsx-a11y/html-has-lang": [
      2
    ],
    "jsx-a11y/iframe-has-title": [
      2
    ],
    "jsx-a11y/img-redundant-alt": [
      2
    ],
    "jsx-a11y/interactive-supports-focus": [
      2
    ],
    "jsx-a11y/label-has-associated-control": [
      2,
      {
        "assert": "both",
        "controlComponents": [],
        "depth": 25,
        "labelAttributes": [],
        "labelComponents": []
      }
    ],
    "jsx-a11y/label-has-for": [
      0,
      {
        "allowChildren": false,
        "components": [],
        "required": {
          "every": [
            "nesting",
            "id"
          ]
        }
      }
    ],
    "jsx-a11y/lang": [
      2
    ],
    "jsx-a11y/media-has-caption": [
      2,
      {
        "audio": [],
        "track": [],
        "video": []
      }
    ],
    "jsx-a11y/mouse-events-have-key-events": [
      2
    ],
    "jsx-a11y/no-access-key": [
      2
    ],
    "jsx-a11y/no-autofocus": [
      2,
      {
        "ignoreNonDOM": true
      }
    ],
    "jsx-a11y/no-distracting-elements": [
      2,
      {
        "elements": [
          "marquee",
          "blink"
        ]
      }
    ],
    "jsx-a11y/no-interactive-element-to-noninteractive-role": [
      2,
      {
        "tr": [
          "none",
          "presentation"
        ]
      }
    ],
    "jsx-a11y/no-noninteractive-element-interactions": [
      2,
      {
        "handlers": [
          "onClick",
          "onMouseDown",
          "onMouseUp",
          "onKeyPress",
          "onKeyDown",
          "onKeyUp"
        ]
      }
    ],
    "jsx-a11y/no-noninteractive-element-to-interactive-role": [
      2,
      {
        "li": [
          "menuitem",
          "option",
          "row",
          "tab",
          "treeitem"
        ],
        "ol": [
          "listbox",
          "menu",
          "menubar",
          "radiogroup",
          "tablist",
          "tree",
          "treegrid"
        ],
        "table": [
          "grid"
        ],
        "td": [
          "gridcell"
        ],
        "ul": [
          "listbox",
          "menu",
          "menubar",
          "radiogroup",
          "tablist",
          "tree",
          "treegrid"
        ]
      }
    ],
    "jsx-a11y/no-noninteractive-tabindex": [
      2,
      {
        "roles": [
          "tabpanel"
        ],
        "tags": []
      }
    ],
    "jsx-a11y/no-onchange": [
      0
    ],
    "jsx-a11y/no-redundant-roles": [
      2
    ],
    "jsx-a11y/no-static-element-interactions": [
      2,
      {
        "handlers": [
          "onClick",
          "onMouseDown",
          "onMouseUp",
          "onKeyPress",
          "onKeyDown",
          "onKeyUp"
        ]
      }
    ],
    "jsx-a11y/role-has-required-aria-props": [
      2
    ],
    "jsx-a11y/role-supports-aria-props": [
      2
    ],
    "jsx-a11y/scope": [
      2
    ],
    "jsx-a11y/tabindex-no-positive": [
      2
    ],
    "promise/always-return": [
      2
    ],
    "promise/catch-or-return": [
      2
    ],
    "promise/no-native": [
      0
    ],
    "promise/param-names": [
      2
    ],
    "react/boolean-prop-naming": [
      0,
      {
        "message": "",
        "propTypeNames": [
          "bool",
          "mutuallyExclusiveTrueProps"
        ],
        "rule": "^(is|has)[A-Z]([A-Za-z0-9]?)+"
      }
    ],
    "react/button-has-type": [
      2,
      {
        "button": true,
        "reset": false,
        "submit": true
      }
    ],
    "react/default-props-match-prop-types": [
      2,
      {
        "allowRequiredDefaults": false
      }
    ],
    "react/destructuring-assignment": [
      0,
      "always"
    ],
    "react/display-name": [
      0,
      {
        "ignoreTranspilerName": false
      }
    ],
    "react/forbid-component-props": [
      0,
      {
        "forbid": []
      }
    ],
    "react/forbid-dom-props": [
      0,
      {
        "forbid": []
      }
    ],
    "react/forbid-elements": [
      0,
      {
        "forbid": []
      }
    ],
    "react/forbid-foreign-prop-types": [
      1,
      {
        "allowInPropTypes": true
      }
    ],
    "react/forbid-prop-types": [
      2,
      {
        "checkChildContextTypes": true,
        "checkContextTypes": true,
        "forbid": [
          "any"
        ]
      }
    ],
    "react/jsx-boolean-value": [
      2,
      "never",
      {
        "always": []
      }
    ],
    "react/jsx-child-element-spacing": [
      0
    ],
    "react/jsx-closing-bracket-location": [
      0,
      "line-aligned"
    ],
    "react/jsx-closing-tag-location": [
      0
    ],
    "react/jsx-curly-brace-presence": [
      2,
      {
        "children": "never",
        "props": "never"
      }
    ],
    "react/jsx-curly-newline": [
      0,
      {
        "multiline": "consistent",
        "singleline": "consistent"
      }
    ],
    "react/jsx-curly-spacing": [
      0,
      "never",
      {
        "allowMultiline": true
      }
    ],
    "react/jsx-equals-spacing": [
      0,
      "never"
    ],
    "react/jsx-filename-extension": [
      2,
      {
        "extensions": [
          ".js",
          ".jsx"
        ]
      }
    ],
    "react/jsx-first-prop-new-line": [
      0,
      "multiline-multiprop"
    ],
    "react/jsx-fragments": [
      2,
      "syntax"
    ],
    "react/jsx-handler-names": [
      0,
      {
        "eventHandlerPrefix": "handle",
        "eventHandlerPropPrefix": "on"
      }
    ],
    "react/jsx-indent": [
      0,
      2
    ],
    "react/jsx-indent-props": [
      0,
      2
    ],
    "react/jsx-key": [
      0
    ],
    "react/jsx-max-depth": [
      0
    ],
    "react/jsx-max-props-per-line": [
      0,
      {
        "maximum": 1,
        "when": "multiline"
      }
    ],
    "react/jsx-no-bind": [
      0,
      {
        "allowArrowFunctions": true,
        "allowBind": false,
        "allowFunctions": false,
        "ignoreDOMComponents": true,
        "ignoreRefs": true
      }
    ],
    "react/jsx-no-comment-textnodes": [
      2
    ],
    "react/jsx-no-duplicate-props": [
      2,
      {
        "ignoreCase": true
      }
    ],
    "react/jsx-no-literals": [
      0,
      {
        "noStrings": true
      }
    ],
    "react/jsx-no-target-blank": [
      2,
      {
        "enforceDynamicLinks": "always"
      }
    ],
    "react/jsx-no-undef": [
      2
    ],
    "react/jsx-one-expression-per-line": [
      0,
      {
        "allow": "single-child"
      }
    ],
    "react/jsx-pascal-case": [
      2,
      {
        "allowAllCaps": true,
        "ignore": []
      }
    ],
    "react/jsx-props-no-multi-spaces": [
      0
    ],
    "react/jsx-props-no-spreading": [
      0,
      {
        "html": "enforce",
        "custom": "enforce",
        "exceptions": []
      }
    ],
    "react/jsx-sort-default-props": [
      0,
      {
        "ignoreCase": true
      }
    ],
    "react/jsx-sort-prop-types": [
      0
    ],
    "react/jsx-sort-props": [
      0,
      {
        "callbacksLast": false,
        "ignoreCase": true,
        "noSortAlphabetically": false,
        "reservedFirst": true,
        "shorthandFirst": false,
        "shorthandLast": false
      }
    ],
    "react/jsx-space-before-closing": [
      0,
      "always"
    ],
    "react/jsx-tag-spacing": [
      0,
      {
        "afterOpening": "never",
        "beforeClosing": "never",
        "beforeSelfClosing": "always",
        "closingSlash": "never"
      }
    ],
    "react/jsx-uses-react": [
      2
    ],
    "react/jsx-uses-vars": [
      2
    ],
    "react/jsx-wrap-multilines": [
      0,
      {
        "arrow": "parens-new-line",
        "assignment": "parens-new-line",
        "condition": "parens-new-line",
        "declaration": "parens-new-line",
        "logical": "parens-new-line",
        "prop": "parens-new-line",
        "return": "parens-new-line"
      }
    ],
    "react/no-access-state-in-setstate": [
      2
    ],
    "react/no-array-index-key": [
      1
    ],
    "react/no-children-prop": [
      2
    ],
    "react/no-danger": [
      1
    ],
    "react/no-danger-with-children": [
      2
    ],
    "react/no-deprecated": [
      2
    ],
    "react/no-did-mount-set-state": [
      0
    ],
    "react/no-did-update-set-state": [
      2
    ],
    "react/no-direct-mutation-state": [
      0
    ],
    "react/no-find-dom-node": [
      2
    ],
    "react/no-is-mounted": [
      2
    ],
    "react/no-multi-comp": [
      0
    ],
    "react/no-redundant-should-component-update": [
      2
    ],
    "react/no-render-return-value": [
      2
    ],
    "react/no-set-state": [
      0
    ],
    "react/no-string-refs": [
      2
    ],
    "react/no-this-in-sfc": [
      2
    ],
    "react/no-typos": [
      2
    ],
    "react/no-unescaped-entities": [
      2
    ],
    "react/no-unknown-property": [
      2
    ],
    "react/no-unsafe": [
      0
    ],
    "react/no-unused-prop-types": [
      2,
      {
        "customValidators": [],
        "skipShapeProps": true
      }
    ],
    "react/no-unused-state": [
      2
    ],
    "react/no-will-update-set-state": [
      2
    ],
    "react/prefer-es6-class": [
      2,
      "always"
    ],
    "react/prefer-read-only-props": [
      0
    ],
    "react/prefer-stateless-function": [
      0,
      {
        "ignorePureComponents": true
      }
    ],
    "react/prop-types": [
      2,
      {
        "customValidators": [],
        "ignore": [],
        "skipUndeclared": false
      }
    ],
    "react/react-in-jsx-scope": [
      2
    ],
    "react/require-default-props": [
      2,
      {
        "forbidDefaultForRequired": true
      }
    ],
    "react/require-optimization": [
      0,
      {
        "allowDecorators": []
      }
    ],
    "react/require-render-return": [
      2
    ],
    "react/self-closing-comp": [
      2
    ],
    "react/sort-comp": [
      2,
      {
        "order": [
          "type-annotations",
          "static-methods",
          "lifecycle",
          "everything-else",
          "render"
        ]
      }
    ],
    "react/sort-prop-types": [
      0,
      {
        "callbacksLast": false,
        "ignoreCase": true,
        "requiredFirst": false,
        "sortShapeProp": true
      }
    ],
    "react/state-in-constructor": [
      2,
      "always"
    ],
    "react/static-property-placement": [
      0,
      "property assignment"
    ],
    "react/style-prop-object": [
      2
    ],
    "react/void-dom-elements-no-children": [
      2
    ]
  },
  "ignorePatterns": [
    "logs",
    "*.log",
    "pids",
    "*.pid",
    "*.seed",
    "lib-cov",
    "coverage",
    ".grunt",
    ".lock-wscript",
    "build/Release",
    ".eslintcache",
    "node_modules",
    ".DS_Store",
    "flow-typed/npm/*",
    "!flow-typed/npm/module_vx.x.x.js",
    "release",
    "app/dist",
    "dll",
    ".idea",
    "npm-debug.log.*",
    "__snapshots__",
    "package.json",
    ".travis.yml",
    "config",
    "dll",
    "flow-typed",
    "internals",
    "resources",
    "app/src/utils/jadn-editor/mitsuketa",
    "app/src/utils/PyodideNode"
  ]
}
Done in 1.95s.
