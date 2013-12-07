'use strict';


module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);
    grunt.initConfig({
        connect: {
            all: {
                options: {
                    base: ['.'],
                    hostname: '*',
                    livereload: true,
                    port: 9000
                }
            }
        },

        watch: {
            all: {
                files: ['.']
            }
        }
    });

    grunt.registerTask('default', ['connect', 'watch']);
};