// jsx-a11y Rules
module.exports = {
  'jsx-a11y/accessible-emoji': 2,
  'jsx-a11y/alt-text': [2, {
    area: [],
    elements: ['img', 'object', 'area', 'input[type=\"image\"]'],
    img: [],
    'input[type=\"image\"]': [],
    object: []
  }],
  'jsx-a11y/anchor-has-content': [2, {
    components: []
  }],
  'jsx-a11y/anchor-is-valid': [2, {
    aspects: ['noHref', 'invalidHref', 'preferButton'],
    components: ['Link'],
    specialLink: ['to']
  }],
  'jsx-a11y/aria-activedescendant-has-tabindex': 2,
  'jsx-a11y/aria-props': 2,
  'jsx-a11y/aria-proptypes': 2,
  'jsx-a11y/aria-role': [2, {
    ignoreNonDOM: false,
    ignoreNonDom: false
  }],
  'jsx-a11y/aria-unsupported-elements': 2,
  'jsx-a11y/autocomplete-valid': [0, {
    inputComponents: []
  }],
  'jsx-a11y/click-events-have-key-events': 2,
  'jsx-a11y/control-has-associated-label': [2, {
    controlComponents: [],
    depth: 5,
    ignoreElements: [
      'audio',
      'canvas',
      'embed',
      'input',
      'textarea',
      'tr',
      'video'
    ],
    ignoreRoles: [
      'grid',
      'listbox',
      'menu',
      'menubar',
      'radiogroup',
      'row',
      'tablist',
      'toolbar',
      'tree',
      'treegrid'
    ],
    labelAttributes: ['label']
  }],
  'jsx-a11y/heading-has-content': [2, {
    components: ['']
  }],
  'jsx-a11y/html-has-lang': 2,
  'jsx-a11y/iframe-has-title': 2,
  'jsx-a11y/img-redundant-alt': 2,
  'jsx-a11y/interactive-supports-focus': 2,
  'jsx-a11y/label-has-associated-control': [2, {
    assert: 'both',
    controlComponents: [],
    depth: 25,
    labelAttributes: [],
    labelComponents: []
  }],
  'jsx-a11y/label-has-for': [0, {
    allowChildren: false,
    components: [],
    required: {
      every: ['nesting', 'id']
    }
  }],
  'jsx-a11y/lang': 2,
  'jsx-a11y/media-has-caption': [2, {
    audio: [],
    track: [],
    video: []
  }],
  'jsx-a11y/mouse-events-have-key-events': 2,
  'jsx-a11y/no-access-key': 2,
  'jsx-a11y/no-autofocus': [2, {
    ignoreNonDOM: true
  }],
  'jsx-a11y/no-distracting-elements': [2, {
    elements: ['marquee', 'blink']
  }],
  'jsx-a11y/no-interactive-element-to-noninteractive-role': [2, {
    tr: ['none', 'presentation']
  }],
  'jsx-a11y/no-noninteractive-element-interactions': [2, {
    handlers: [
      'onClick',
      'onMouseDown',
      'onMouseUp',
      'onKeyPress',
      'onKeyDown',
      'onKeyUp'
    ]
  }],
  'jsx-a11y/no-noninteractive-element-to-interactive-role': [2, {
    li: ['menuitem', 'option', 'row', 'tab', 'treeitem'],
    ol: [
      'listbox',
      'menu',
      'menubar',
      'radiogroup',
      'tablist',
      'tree',
      'treegrid'
    ],
    table: ['grid'],
    td: ['gridcell'],
    ul: [
      'listbox',
      'menu',
      'menubar',
      'radiogroup',
      'tablist',
      'tree',
      'treegrid'
    ]
  }],
  'jsx-a11y/no-noninteractive-tabindex': [2, {
    roles: ['tabpanel'],
    tags: []
  }],
  'jsx-a11y/no-onchange': 0,
  'jsx-a11y/no-redundant-roles': 2,
  'jsx-a11y/no-static-element-interactions': [2, {
    handlers: [
      'onClick',
      'onMouseDown',
      'onMouseUp',
      'onKeyPress',
      'onKeyDown',
      'onKeyUp'
    ]
  }],
  'jsx-a11y/role-has-required-aria-props': 2,
  'jsx-a11y/role-supports-aria-props': 2,
  'jsx-a11y/scope': 2,
  'jsx-a11y/tabindex-no-positive': 2
};
