<p align="center">
  <a href="./src/logo.png">
    <img src="./src/logo.png" />
   </a>
  <br/>
  <a href="https://www.npmjs.com/package/css-loading">
    <img src="http://img.shields.io/npm/v/css-loading.svg" />
   </a>
  <a href="https://www.npmjs.com/package/css-loading">
    <img src="https://img.shields.io/bower/v/css-loading.svg" />
   </a>
  <a href="https://www.npmjs.com/package/css-loading">
    <img src="http://img.shields.io/npm/dm/css-loading.svg" />
   </a>
  <a href="https://github.com/jovey-zheng/loader/blob/master/LICENSE">
    <img src="https://img.shields.io/npm/l/css-loading.svg" />
   </a>
</p>

<p align="center">
Pure css loading animations. As long as only one element! <a href="http://jovey-zheng.github.io/loader">Live Demos</a>.
</p>
<p align="center">
Inspiration from <a href="https://github.com/ConnorAtherton/loaders.css">loaders.css</a> and <a href="https://github.com/lukehaas/css-loaders">css-loaders</a>.
</p>


## Install

Install with npm:
  ```
  $ npm install --save css-loading
  ```

install with bower:
  ```
  $ bower install --save css-loading
  ```

or download [the Latest releases version(ZIP)](https://github.com/jovey-zheng/loader/archive/v1.4.0.zip).

## Basic Usage

1. Import:

  ```html
  <link rel="stylesheet" href="loaders.css"> or
  <link rel="stylesheet" href="loaders.min.css">
  ```

  or require from `node_modules`:

  ```js
  import 'css-loading'
  ```

2. Create an element and add the attribute `data-loader`:

  ```html
  <div data-loader="circle"></div>
  ```

## Contributing

Pull requests are welcome!

Create another animation file in `src/` and test it in `example/example.html`, then open it in a browser to see your animation running.

## License

License under [MIT](https://github.com/jovey-zheng/loader/blob/master/LICENSE).
