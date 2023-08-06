import io
import os

from flask import render_template, request, send_file

from eagle.application import app
from eagle.views.common import sample_filename, available_sample_objects, \
    parse_request, available_groups, group_filename, available_group_samples
try:
    from eagle.core import motif as core_motif
    __matplotlib_installed = True
except ImportError:
    __matplotlib_installed = False


def samples_by_diseases(diseases):
    '''return all samples affected by one of the given diseases'''
    samples = [sample_filename(s.basename) for s in available_sample_objects()
               if '@'+s.disease in diseases]
    for disease in diseases:
        if not disease.startswith('@'):
            file_path = group_filename(disease)
            group_samples = available_group_samples(file_path)
            samples += [sample_filename(sample) for sample in group_samples]
    return samples


@app.route('/motif', methods=['GET', 'POST'])
def motif():
    if request.method != "POST":
        if __matplotlib_installed:
            return render_template(
                'motif_query.html',
                available_samples=available_sample_objects(),
                available_groups=available_groups())
        else:
            return render_template('install_matplotlib.html')

    q = parse_request(request)
    cases = [sample_filename(c) for c in q.case]
    cases.extend(samples_by_diseases(q.case_groups))
    controls = [sample_filename(c) for c in q.control]
    controls.extend(samples_by_diseases(q.control_groups))
    core_motif.main(cases, controls, q.uuid)

    return render_template('motif_results.html', query=q)


@app.route('/images/motif/<name>')
def motif_images(name):
    if not os.path.exists("/tmp/eagle"):
        os.mkdir("/tmp/eagle")
    f = open("/tmp/eagle/" + name, "rb")
    os.remove("/tmp/eagle/" + name)

    return send_file(io.BytesIO(f.read()),
                     attachment_filename=name,
                     mimetype='image/png')
