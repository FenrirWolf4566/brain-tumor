
/*jslint browser: true, node: true */
/*global require, module, describe, it */

/*NIfTI files can be single file (.nii) or pairs (.hdr; .img) */
/*To create paired NIfTI images */
/*  $ FSLOUTPUTTYPE=NIFTI_PAIR_GZ */
/*  $ fslmaths AIR.nii.gz -add 0 air */

/* If you can support paired files you must pass `true` as second parameter: */
/* isNIFTI2() isNIFTI1(), isNIFTI() */
/* you must read two files (header and image), in this example buf and ibuf */

"use strict";

var assert = require("assert");
var fs = require('fs');

var nifti = require('../src/nifti.js');

var buf = fs.readFileSync('./tests/data/air.hdr.gz');
var data = nifti.Utils.toArrayBuffer(buf);
var ibuf = fs.readFileSync('./tests/data/air.img.gz');
var idata = nifti.Utils.toArrayBuffer(ibuf);

var nifti1 = null;
var bytes = null;
var clone = null;
describe('NIFTI-Reader-JS', function () {
    describe('uncompressed nifti-1 hdr/img pair test', function () {
        it('isCompressed() should return true', function () {
            assert.equal(true, nifti.isCompressed(idata));
        });


        it('should not throw error when decompressing header', function (done) {
            assert.doesNotThrow(function() {
                data = nifti.decompress(data);
                done();
            });
        });

        it('should not throw error when decompressing image', function (done) {
            assert.doesNotThrow(function() {
                idata = nifti.decompress(idata);
                done();
            });
        });

        it('isNIFTI1() should return true', function () {
            assert.equal(true, nifti.isNIFTI1(data, true));
        });

        it('isNIFTI() should return true', function () {
            assert.equal(true, nifti.isNIFTI(data, true));
        });

        it('should not throw error when reading header', function (done) {
            assert.doesNotThrow(function() {
                nifti1 = nifti.readHeader(data, true);
                done();
            });
        });

        it('dims[1] should be 79', function () {
            assert.equal(79, nifti1.dims[1]);
        });

        it('dims[2] should be 67', function () {
            assert.equal(67, nifti1.dims[2]);
        });

        it('dims[3] should be 64', function () {
            assert.equal(64, nifti1.dims[3]);
        });

        it('image data checksum should equal 692149477', function () {
            var imageData = nifti.readImage(nifti1, idata);
            var checksum = nifti.Utils.crc32(new DataView(imageData));
            assert.equal(checksum, 692149477);
        });

        it('data returned from toArrayBuffer preserves all nifti-1 properties', function() {
            nifti1 = nifti.readHeader(data, true);
            bytes = nifti1.toArrayBuffer();
            clone = nifti.readHeader(bytes, true);
            assert.deepEqual(clone, nifti1);
        });

    });

});
