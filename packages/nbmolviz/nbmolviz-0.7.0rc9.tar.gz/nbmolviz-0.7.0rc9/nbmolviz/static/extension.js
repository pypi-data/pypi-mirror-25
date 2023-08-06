define(function() { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

	// TEMPLATE FROM https://github.com/jupyter/widget-cookiecutter

	// This file contains the javascript that is run when the notebook is loaded.
	// It contains some requirejs configuration and the `load_ipython_extension`
	// which is required for any notebook extension.

	// Configure requirejs
	if (window.require) {
	    window.require.config({
	        map: {
	            "*" : {
	                "nbmolviz-js": "nbextensions/nbmolviz-js/index",
	                "jupyter-js-widgets": "nbextensions/jupyter-js-widgets/extension"
	            }
	        }
	    });
	}

	function loadJupyterExtension () {
	    // Load CSS:
	    $('<link/>')
	        .appendTo('head')
	        .attr({
	            id: 'nbmolviz_css',
	            rel: 'stylesheet',
	            type: 'text/css',
	            href: window.require.toUrl('nbextensions/nbmolviz-js/nbmolviz.css')
	        });
	}

	// Export the required load_ipython_extension
	module.exports = {
	    load_ipython_extension: loadJupyterExtension
	};


/***/ })
/******/ ])});;