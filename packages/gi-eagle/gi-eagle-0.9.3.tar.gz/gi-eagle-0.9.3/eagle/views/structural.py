"""
The structural page
"""
from flask import render_template, request

from eagle.application import app
from eagle.core import structural as core_structural
from eagle.views.common import sample_filename, available_sample_objects,\
    parse_request, available_chromosomes


@app.route('/structural', methods=['GET', 'POST'])
def structural():
    if request.method != "POST":
        return render_template(
            'structural_query.html',
            available_samples=available_sample_objects(),
            available_chromosomes=available_chromosomes(),
        )

    q = parse_request(request)
    case_files = [sample_filename(c) for c in q.case]

    results = core_structural.run(case_files, q.chromosomes, q.insertion,
                                  q.inversion, q.deletion,
                                  q.min_variant_length, q.max_variant_length)

    return render_template('structural_results.html', results=results, query=q)
