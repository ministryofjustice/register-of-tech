var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat-css');
var del = require('del');
var runSequence = require('run-sequence');

gulp.task('govuk-styles', function() {
  return gulp.src('./rot/static-src/stylesheets/scss/govuk/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./rot/static-src/stylesheets/css/govuk'))
});

gulp.task('app-styles', function() {
  return gulp.src('./rot/static-src/stylesheets/scss/application/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(concat('application.css'))
    .pipe(gulp.dest('./rot/static-src/stylesheets/css'))
});

gulp.task('clean', function() {
  return del('./rot/static-src/stylesheets/css');
});

gulp.task('sass', function() {
  runSequence('clean', 'govuk-styles', 'app-styles');
});

gulp.task('watch', ['sass'], function() {
  gulp.watch('./rot/static-src/stylesheets/scss/**/*.scss', ['sass']);
});
