#!/usr/bin/env python

# Joe Gillotti - 7/25/2017
# Because https://github.com/dnbert/prm has unresolved issues and I wanted
# something lean and fast.

import os
import gzip
import argparse
import shutil
import hashlib
import sys
import json
from email.Utils import formatdate


def get_deb_package_class():
    DebPackage = None
    try:
        from apt.debfile import DebPackage
    except ImportError:
        pass
    else:
        return DebPackage

    # if we're in a venv, this won't be in our path by default,
    # so add it and try to import it after that.
    if os.path.exists('/usr/lib/python2.7/dist-packages/apt'):
        import site
        site.addsitedir('/usr/lib/python2.7/dist-packages')

        try:
            from apt.debfile import DebPackage
        except ImportError:
            pass
        else:
            return DebPackage

    print 'Please run apt-get install python-apt (or try running this outside of a venv)'
    sys.exit(1)


DebPackage = get_deb_package_class()
subpath_format = 'dists/{suite}/{category}/{arch}'


def deb_hashcache_path(deb_path):
    root = os.path.dirname(deb_path)
    name = os.path.basename(deb_path)

    # chunk the subfolder into subfolders 5 levels down. trivial way of trying to avoid too many files in
    # one folder which can cause serious file system performance degredation. it's possible another
    # bucketing strategy would be better.
    chunk_size = 5
    tokens = [name[pos:pos + chunk_size] for pos in xrange(0, len(name), chunk_size)]

    cache_path = os.path.join(root, '.hash_cache')
    for token in tokens:
        cache_path = os.path.join(cache_path, token)
    cache_path = os.path.join(cache_path, 'digests.json')

    return cache_path


def get_digests(deb_path):
    cache_path = deb_hashcache_path(deb_path)

    # If we have these digests cached for this deb, and if the deb isn't
    # newer, just use that instead.
    if os.path.exists(cache_path):
        if os.path.getmtime(cache_path) > os.path.getmtime(deb_path):
            try:
                with open(cache_path, 'r') as h:
                    return json.load(h)
            except (IOError, ValueError) as e:
                print 'Failed loading cache from file %s: %s' % (cache_path, e)

    # populate each digest at once to avoid reading the file multiple times.
    md5_digest = hashlib.md5()
    sha1_digest = hashlib.sha1()
    sha256_digest = hashlib.sha256()

    try:
        with open(deb_path) as h:
            while True:
                buff = h.read(1024)
                if buff == '':
                    break
                md5_digest.update(buff)
                sha1_digest.update(buff)
                sha256_digest.update(buff)
    except IOError as e:
        print 'Failed opening %s to generate hashes. Will use blank hashes, which may cause problems. %s' % (deb_path, e)
        return {
            'md5': '',
            'sha1': '',
            'sha256': '',
        }

    result = {
        'md5': md5_digest.hexdigest(),
        'sha1': sha1_digest.hexdigest(),
        'sha256': sha256_digest.hexdigest(),
    }

    try:
        if not os.path.exists(os.path.dirname(cache_path)):
            os.makedirs(os.path.dirname(cache_path))
        with open(cache_path, 'w') as h:
            json.dump(result, h, indent=2)
    except (IOError, OSError) as e:
        print 'Failed writing cached hash to %s: %s' % (cache_path, e)

    return result


def pathstrip(path, tostrip):
    if path.find(tostrip) == 0:
        path = path[len(tostrip) + 1:]
    return path


def get_debs(root):
    for filename in os.listdir(root):
        path = os.path.join(root, filename)
        if path.endswith('.deb'):
            yield path


def generate_package_block(path, filename):
    digests = get_digests(path)
    parts = []
    parts.append(DebPackage(path).control_content('control').strip())
    parts.append('Filename: %s' % filename)
    parts.append('MD5sum: %s' % digests['md5'])
    parts.append('SHA1: %s' % digests['sha1'])
    parts.append('SHA256: %s' % digests['sha256'])
    parts.append('Size: %s' % os.path.getsize(path))
    return '\n'.join(parts)


def generate_indexes(path, suite, category, arch, newpackages=None):
    arch = 'binary-%s' % arch

    subpath = os.path.join(path, subpath_format.format(suite=suite, category=category, arch=arch))

    if not os.path.exists(subpath):
        os.makedirs(subpath)

    if newpackages and os.path.exists(newpackages):
        for filename in os.listdir(newpackages):
            if not filename.endswith('.deb'):
                continue
            old_path = os.path.join(newpackages, filename)
            dest_path = os.path.join(subpath, filename)
            if os.path.exists(dest_path):
                print 'Skipping already found package %s' % old_path
            else:
                print 'Moving %s to %s' % (old_path, dest_path)
                try:
                    shutil.move(old_path, dest_path)
                except (IOError, OSError) as e:
                    print 'Failed moving %s. Just copying instead. %s' % (old_path, e)
                    try:
                        shutil.copyfile(old_path, dest_path)
                    except (IOError, OSError) as e:
                        print 'Failed copying %s to %s: %s' % (old_path, dest_path, e)

    packages_file = os.path.join(path, 'dists', suite, category, arch, 'Packages')
    packages_file_gz = packages_file + '.gz'

    release_file = os.path.join(path, 'dists', suite, 'Release')
    release_trimto = os.path.join(path, 'dists', suite)

    print 'Generating %s' % packages_file
    with open(packages_file, 'w') as h:
        for deb in get_debs(subpath):
            print 'Processing %s' % deb
            filename = pathstrip(deb, path)
            try:
                data = generate_package_block(deb, filename)
            except (IOError, SystemError) as e:
                print '%s failed: %s. Skipping.' % (deb, e)
                continue
            h.write(data)
            h.write('\n\n')

    print 'Generating %s' % packages_file_gz
    with open(packages_file, 'r') as source:
        with gzip.open(packages_file_gz, 'wb') as dest:
            while True:
                buff = source.read(1024)
                if buff == '':
                    break
                dest.write(buff)

    print 'Generating %s' % release_file
    release_sources = {
        packages_file: get_digests(packages_file),
        packages_file_gz: get_digests(packages_file_gz)
    }
    hashes = (('MD5Sum', 'md5'), ('SHA1', 'sha1'), ('SHA256', 'sha256'))
    with open(release_file, 'w') as h:
        h.write('Date: %s\n' % formatdate())
        h.write('Suite: %s\n' % suite)

        for label, kind in hashes:
            h.write('%s:\n' % label)
            for filename in release_sources:
                size = os.path.getsize(filename)
                h.write(' %-64s %s %s\n' % (release_sources[filename][kind], size, pathstrip(filename, release_trimto)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--suite', help='eg: trusty', required=True)
    parser.add_argument('-c', '--category', help='eg: main', required=True)
    parser.add_argument('-a', '--arch', help='amd64', required=True)
    parser.add_argument('-p', '--path', help='path to debian repo', required=True)
    parser.add_argument('-n', '--newpackages', help='path to folder full of new debs. (omit to just regenerate indexes)')
    args = parser.parse_args()
    generate_indexes(**dict(args._get_kwargs()))


if __name__ == '__main__':
    main()
