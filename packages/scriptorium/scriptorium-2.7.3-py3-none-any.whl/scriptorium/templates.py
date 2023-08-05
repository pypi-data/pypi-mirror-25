#!/usr/bin/env python
"""Tools for reasoning over templates."""

import subprocess
import re
import os
import os.path
import yaml

import scriptorium

def all_templates(dname=None):
    """Builds list of installed templates."""
    if not dname or not os.path.exists(dname):
        dname = scriptorium.CONFIG['TEMPLATE_DIR']
    templates = []
    for dirpath, _, filenames in os.walk(dname):
        if 'setup.tex' in filenames:
            templates.append(os.path.basename(dirpath))

    return templates

def find_template(tname, template_dir=None):
    """Searches given template directory for the named template."""
    template_dir = template_dir if template_dir else scriptorium.CONFIG['TEMPLATE_DIR']
    for dirpath, _, _ in os.walk(template_dir):
        if os.path.basename(dirpath) == tname:
            return os.path.join(template_dir, dirpath)
    raise IOError('{0} cannot be found in {1}'.format(tname, template_dir))

def repo_checkout(repo, rev):
    """Checks out a specific revision of the repository."""
    old_cwd = os.getcwd()
    os.chdir(repo)
    subprocess.check_call(['git', 'checkout', rev])
    os.chdir(old_cwd)

def install_template(url, template_dir=None, rev=None):
    """Installs a template in the template_dir, optionally selecting a revision."""
    url_re = re.compile(r'((git|ssh|http(s)?)(:(//)?)|([\w\d]*@))?(?P<url>[\w\.]+).*\/(?P<dir>[\w\-]+)(\.git)(/)?')
    match = url_re.search(url)
    if not match:
        raise ValueError('{0} is not a valid git URL'.format(url))
    template = match.group('dir')
    template_dir = template_dir if template_dir else scriptorium.CONFIG['TEMPLATE_DIR']
    template_dest = os.path.join(template_dir, template)

    if os.path.exists(template_dest):
        raise IOError('{0} already exists, cannot install on top'.format(template))

    try:
        subprocess.check_output(['git', 'clone', url, template_dest], universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        raise IOError('\n'.join(['Could not clone template:', exc.output]))

    treeish_re = re.compile(r'[A-Za-z0-9_\-\.]+')
    if rev and treeish_re.match(rev):
        repo_checkout(template_dest, rev)

def update_template(template, template_dir=None, rev=None):
    """Updates the given template repository."""
    template_loc = find_template(template, template_dir)

    old_cwd = os.getcwd()
    os.chdir(template_loc)
    try:
        subprocess.check_call(['git', 'fetch', 'origin'])
        git_cmd = ['git', 'symbolic-ref', '--short', 'HEAD']
        current_rev = subprocess.check_output(git_cmd, universal_newlines=True)
        current_rev = current_rev.rstrip()
        rev = rev if rev else current_rev
        treeish_re = re.compile(r'[A-Za-z0-9_\-\.]+')
        if treeish_re.match(rev):
            if rev != current_rev:
                subprocess.check_call(['git', 'checkout', rev])
            subprocess.check_call(['git', 'pull', 'origin', rev])
    except subprocess.CalledProcessError as exc:
        raise IOError('Cannot update {0}:\n {1}'.format(template, exc.output))
    os.chdir(old_cwd)

def list_variables(template, template_dir=None):
    """List variables a template offers for paper creation."""
    template_dir = template_dir if template_dir else scriptorium.CONFIG['TEMPLATE_DIR']

    template_loc = find_template(template, template_dir)

    var_re = re.compile(r'\$(?P<var>[A-Z0-9]+)')

    files = [os.path.join(template_loc, 'frontmatter.mmd'),
             os.path.join(template_loc, 'metadata.tex')
            ]
    variables = []
    for test_file in files:
        try:
            with open(test_file, 'r') as fp:
                for match in re.finditer(var_re, fp.read()):
                    if match.group('var') != 'TEMPLATE':
                        variables.append(match.group('var'))
        except EnvironmentError:
            pass
    return list(set(variables))

def get_manifest(template, template_dir=None):
    """
    Get manifest for a given template with keys as output names, and values as input names.

    This list of files defines which files should be used when creating a new paper using this document.
    """
    template_dir = template_dir if template_dir else scriptorium.CONFIG['TEMPLATE_DIR']
    template_loc = find_template(template, template_dir)
    manifest_path = os.path.join(template_loc, 'manifest.yml')
    manifest = {
        'paper.mmd': 'frontmatter.mmd',
        'metadata.tex': 'metadata.tex'
        }

    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as mfp:
            manifest = yaml.load(mfp)

    #Remove non-existent files from manifest list
    manifest = {kk:vv for kk, vv in manifest.items() if os.path.exists(os.path.join(template_loc, vv))}
    return manifest

def get_default_config(template, template_dir=None):
    """Get default configuration options if available."""
    template_dir = template_dir if template_dir else scriptorium.CONFIG['TEMPLATE_DIR']
    template_loc = find_template(template, template_dir)
    config_path = os.path.join(template_loc, 'default_config.yml')
    config = {}

    if os.path.exists(config_path):
        with open(config_path, 'r') as cfp:
            raw_config = yaml.load(cfp)
        config = {kk.upper(): vv for kk, vv in raw_config.items()}
    return config
