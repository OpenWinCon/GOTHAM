module.exports = function (grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      dev: {
        files: {
          'pipe/js/main.js': [
            'src/scripts/base.js',
          ],
        },
        options: {
          sourceMap: false,
          sourceMapStyle: 'inline'
        }
      },

      css: {
        files: {
          'pipe/css/gotham.css': [
            'src/styles/base.css',
            'pipe/css/main.css',
            'bower_components/bootstrap/dist/css/bootstrap.css',
            'bower_components/font-awesome/css/font-awesome.css',
            'bower_components/adminlte/dist/css/AdminLTE.css',
            'bower_components/adminlte/dist/css/skins/skin-yellow-light.css',
          ],
        },
        options: {
          sourceMap: false,
          sourceMapStyle: 'inline'
        }
      },

      'dev-lib': {
        files: {
          'pipe/js/lib.js': [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/jquery-validation/dist/jquery.validate.js',
            'bower_components/jquery-validation/dist/additional-methods.js',
            'bower_components/jquery-validation/src/localization/messages_en.js',
            'bower_components/bootstrap/dist/js/bootstrap.js',
            'bower_components/adminlte/plugins/slimScroll/jquery.slimScroll.js',
            'bower_components/adminlte/plugins/fastclick/fastclick.js',
            'bower_components/adminlte/dist/js/app.js',
          ]
        }
      }
    },

    jshint: {
      all: ['src/scripts/*'],
      options: {
        jshintrc: true,
        force: true,
        browser: true
      }
    },

    uglify: {
      build: {
        files: [{
          'public/js/gotham.min.js': [
            'pipe/js/lib.js',
            'pipe/js/main.js'
          ],
        },{
          expand: true,
          src: ["*.js", "!base.js"],
          dest: "public/js",
          ext: ".min.js",
          cwd: "src/scripts"
        }],
        options: {
          mangle: true,
          compress: true
        }
      }
    },

    cssmin: {
      options: {
        compatibility: {
          properties: { zeroUnits: false }
        }
      },
      build: {
        files: [{
          'public/css/gotham.min.css': [
            'pipe/css/gotham.css'
          ],
        }, {
            cwd: "src/styles/",
            src: ["*.css", "!base.css"],
            dest: "public/css",
            expand: true,
            ext: ".min.css",
        }]
      }
    },

    less: {
      dev: {
        files: {
          'pipe/css/main.css': [
            'src/styles/main.less'
          ]
        }
      }
    },

    pug: {
      compile: {
        files: [
          {
            cwd: "src/views/",
            src: "*.jade",
            dest: "public",
            expand: true,
            ext: ".html"
          }
        ],
        options: {
          pretty: true,
          data: {
            debug: false
          }
        }
      }
    },

    watch: {
      html: {
        files: ['src/views/**/*.jade'],
        tasks: ['pug:compile']
      },
      scripts: {
        files: ['src/scripts/*.js'],
        tasks: ['concat:dev', 'uglify:build']
      },
      less: {
        files: ['src/styles/*.less', 'src/styles/*.css'],
        tasks: ['less:dev', 'concat:css', 'cssmin:build']
      },
      options: {
        livereload: false
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-pug');

  grunt.registerTask('dev', ['concat:dev', 'concat:dev-lib', 'uglify:build', 'less:dev', 'concat:css', 'cssmin:build', 'pug:compile', 'watch']);
  grunt.registerTask('build', ['jshint', 'concat:dev', 'concat:dev-lib','uglify:build', 'less:dev', 'concat:css', 'cssmin:build', 'pug:compile']);
  grunt.registerTask('lint', ['concat:dev', 'concat:dev-lib', 'uglify:build', 'jshint']);
};
