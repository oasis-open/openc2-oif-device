// React Rules

module.exports = {
  'react/boolean-prop-naming': [0, {
    message: '',
    propTypeNames: ['bool', 'mutuallyExclusiveTrueProps'],
    rule: '^(is|has)[A-Z]([A-Za-z0-9]?)+'
  }],
  'react/button-has-type': [2, {
    button: true,
    reset: false,
    submit: true
  }],
  'react/default-props-match-prop-types': [2, {
    allowRequiredDefaults: false
  }],
  'react/destructuring-assignment': [0, 'always'],
  'react/display-name': [0, {
    ignoreTranspilerName: false
  }],
  'react/forbid-component-props': [0, {
    forbid: []
  }],
  'react/forbid-dom-props': [0, {
    forbid: []
  }],
  'react/forbid-elements': [0, {
    forbid: []
  }],
  'react/forbid-foreign-prop-types': [1, {
    allowInPropTypes: true
  }],
  'react/forbid-prop-types': [2, {
    checkChildContextTypes: true,
    checkContextTypes: true,
    forbid: ['any']
  }],
  'react/jsx-boolean-value': [2, 'never', {
    always: []
  }],
  'react/jsx-child-element-spacing': 0,
  'react/jsx-closing-bracket-location': [0, 'line-aligned'],
  'react/jsx-closing-tag-location': 0,
  'react/jsx-curly-brace-presence': [2, {
    children: 'never',
    props: 'never'
  }],
  'react/jsx-curly-newline': [0, {
    multiline: 'consistent',
    singleline: 'consistent'
  }],
  'react/jsx-curly-spacing': [0, 'never', {
    allowMultiline: true
  }],
  'react/jsx-equals-spacing': [0, 'never'],
  'react/jsx-filename-extension': [2, {
    extensions: ['.js', '.jsx']
  }],
  'react/jsx-first-prop-new-line': [0, 'multiline-multiprop'],
  'react/jsx-fragments': [2, 'syntax'],
  'react/jsx-handler-names': [0, {
    eventHandlerPrefix: 'handle',
    eventHandlerPropPrefix: 'on'
  }],
  'react/jsx-indent': [0, 2],
  'react/jsx-indent-props': [0, 2],
  'react/jsx-key': 0,
  'react/jsx-max-depth': 0,
  'react/jsx-max-props-per-line': [0, {
    maximum: 1,
    when: 'multiline'
  }],
  'react/jsx-no-bind': [0, {
    allowArrowFunctions: true,
    allowBind: false,
    allowFunctions: false,
    ignoreDOMComponents: true,
    ignoreRefs: true
  }],
  'react/jsx-no-comment-textnodes': 2,
  'react/jsx-no-duplicate-props': [2, {
    ignoreCase: true
  }],
  'react/jsx-no-literals': [0, {
    noStrings: true
  }],
  'react/jsx-no-target-blank': [2, {
    enforceDynamicLinks: 'always'
  }],
  'react/jsx-no-undef': 2,
  'react/jsx-one-expression-per-line': [0, {
    allow: 'single-child'
  }],
  'react/jsx-pascal-case': [2, {
    allowAllCaps: true,
    ignore: []
  }],
  'react/jsx-props-no-multi-spaces': 0,
  'react/jsx-props-no-spreading': 0,
  'react/jsx-sort-default-props': [0, {
    ignoreCase: true
  }],
  'react/jsx-sort-prop-types': 0,
  'react/jsx-sort-props': [0, {
    callbacksLast: false,
    ignoreCase: true,
    noSortAlphabetically: false,
    reservedFirst: true,
    shorthandFirst: false,
    shorthandLast: false
  }],
  'react/jsx-space-before-closing': [0, 'always'],
  'react/jsx-tag-spacing': [0, {
    afterOpening: 'never',
    beforeClosing: 'never',
    beforeSelfClosing: 'always',
    closingSlash: 'never'
  }],
  'react/jsx-uses-react': 2,
  'react/jsx-uses-vars': 2,
  'react/jsx-wrap-multilines': [0, {
    arrow: 'parens-new-line',
    assignment: 'parens-new-line',
    condition: 'parens-new-line',
    declaration: 'parens-new-line',
    logical: 'parens-new-line',
    prop: 'parens-new-line',
    return: 'parens-new-line'
  }],
  'react/no-access-state-in-setstate': 2,
  'react/no-array-index-key': 1,
  'react/no-children-prop': 2,
  'react/no-danger': 1,
  'react/no-danger-with-children': 2,
  'react/no-deprecated': 2,
  'react/no-did-mount-set-state': 0,
  'react/no-did-update-set-state': 2,
  'react/no-direct-mutation-state': 0,
  'react/no-find-dom-node': 2,
  'react/no-is-mounted': 2,
  'react/no-multi-comp': 0,
  'react/no-redundant-should-component-update': 2,
  'react/no-render-return-value': 2,
  'react/no-set-state': 0,
  'react/no-string-refs': 2,
  'react/no-this-in-sfc': 2,
  'react/no-typos': 2,
  'react/no-unescaped-entities': 2,
  'react/no-unknown-property': 2,
  'react/no-unsafe': 0,
  'react/no-unused-prop-types': [2, {
    customValidators: [],
    skipShapeProps: true
  }],
  'react/no-unused-state': 2,
  'react/no-will-update-set-state': 2,
  'react/prefer-es6-class': [2, 'always'],
  'react/prefer-read-only-props': 0,
  'react/prefer-stateless-function': [0, {
    ignorePureComponents: true
  }],
  'react/prop-types': [2, {
    customValidators: [],
    ignore: [],
    skipUndeclared: false
  }],
  'react/react-in-jsx-scope': 2,
  'react/require-default-props': [2, {
    forbidDefaultForRequired: true
  }],
  'react/require-optimization': [0, {
    allowDecorators: []
  }],
  'react/require-render-return': 2,
  'react/self-closing-comp': 2,
  'react/sort-comp': [2, {
    order: [
      'type-annotations',
      'static-methods',
      'lifecycle',
      'everything-else',
      'render'
    ]
  }],
  'react/sort-prop-types': [0, {
    callbacksLast: false,
    ignoreCase: true,
    requiredFirst: false,
    sortShapeProp: true
  }],
  'react/state-in-constructor': [2, 'always'],
  'react/static-property-placement': [0, 'property assignment'],
  'react/style-prop-object': 2,
  'react/void-dom-elements-no-children': 2
}