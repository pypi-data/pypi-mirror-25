hoist-prop-types
=========

A codemod that will hoist prop types and default props to the top of the file. 
Currently only works with files with one component.

### Motivation
The main purpose is to bring the more important parts of your components, `propTypes`, 
to the top of the file.  PropTypes help explains what your component does, almost as 
much as the render method.  Keeping them close to the top of your file helps minimize 
scrolling and keeps your code that much more consistent. 


### Input:
```javascript
import * as React from 'react';
import PropTypes from 'prop-types';

class MyComponent extends React.Component {
  render() { return null; }
}

MyComponent.propTypes = {
  name: PropTypes.string,
};
MyComponent.defaultProps = {
  name: 'Jim'
};
```

### Output:
```javascript
import * as React from 'react';
import PropTypes from 'prop-types';

const PROPS = {
   name: PropTypes.string,
};

const DEFAULT_PROPS = {
   name: 'Jim'
};

class MyComponent extends React.Component {
  render() { return null; }
}

MyComponent.propTypes = PROPS;
MyComponent.defaultProps = DEFAULT_PROPS;

```

`hoist-prop-types` will work with `static propTypes ={...}` that are delared in the class as well.

Install
-----------
```
pip install hoist-prop-types
```

Usage
----------
```
hoist-prop-types ./my/dir/
```

This will read all `.js` and `.jsx` files and try to hoist the prop types to the top.

