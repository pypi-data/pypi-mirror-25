hoist-prop-types
=========

A codemod that will hoist prop types and default props to the top of the file.  Currently only
works with files with one component.

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
