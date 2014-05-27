var gulp = require('gulp');
var filelog = require('gulp-filelog');
var filter = require('gulp-filter');
var rename = require('gulp-rename'); // https://github.com/hparra/gulp-rename
var less = require('gulp-less');
var minifycss = require('gulp-minify-css');

var handleError = function (err) {  console.log(err.message);  this.emit('end');  };

gulp.task('less', function() {
    return gulp.src([
        'static/less/m.less'
      ])
        .pipe( less() )
          .on('error', handleError)
        .pipe( minifycss({ keepBreaks:true, compatibility:'ie8' }) )
          .on('error', handleError)
        .pipe( rename(function(path){  path.basename = path.basename.replace(/^__/, '');  }) )
        .pipe( gulp.dest('static/css') );
  });

gulp.task('watch', function() {
    gulp.watch('static/less/**.less', ['less']);
  });

gulp.task('default', ['less', 'watch']);