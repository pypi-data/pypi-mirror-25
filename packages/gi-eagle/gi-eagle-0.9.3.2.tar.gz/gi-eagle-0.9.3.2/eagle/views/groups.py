import os

from flask import render_template, request

from eagle.application import app
from eagle.core.groups import create_group, delete_group
from eagle.views.common import GROUP_PATH, available_groups, group_filename,\
    available_sample_objects, available_group_samples, Query


@app.route("/groups", methods=['GET', 'POST'])
def groups():
    sample_to_index = {sample: index for index, sample
                       in enumerate(available_sample_objects())}
    if request.method != "POST":
        return render_template(
            "groups.html",
            sample_to_index=sample_to_index,
            available_samples=available_sample_objects(),
            groups=available_groups(),
            group_samples={g: available_group_samples(group_filename(g))
                           for g in available_groups()})

    action = request.form.get('action')
    if action == 'create':
        args = Query()
        args.group = group_filename(request.form.get('group'))
        args.sample = request.form.getlist('samples')
        if os.path.abspath(args.group).startswith(GROUP_PATH):
            create_group(args)
            message = "Created group %s" % args.group
            return render_template(
                "groups.html",
                sample_to_index=sample_to_index,
                available_samples=available_sample_objects(),
                groups=available_groups(),
                group_samples={g: available_group_samples(group_filename(g))
                               for g in available_groups()},
                message=message,
                error=False)

        message = "Could not create group %s" % args.group
        return render_template(
            "groups.html",
            sample_to_index=sample_to_index,
            available_samples=available_sample_objects(),
            groups=available_groups(),
            group_samples={g: available_group_samples(group_filename(g))
                           for g in available_groups()},
            message=message,
            error=True)

    elif action == 'update':
        args = Query()
        args.group = group_filename(request.form.get('group'))
        args.sample = request.form.getlist('samples')
        submit = request.form.get('submit')
        if submit == 'submit':
            if os.path.abspath(args.group).startswith(GROUP_PATH):
                create_group(args)
                message = "Updated group %s" % args.group
                return render_template(
                    "groups.html",
                    sample_to_index=sample_to_index,
                    available_samples=available_sample_objects(),
                    groups=available_groups(),
                    group_samples={
                        g: available_group_samples(group_filename(g))
                        for g in available_groups()
                    },
                    message=message,
                    error=False)

            message = "Could not update group %s" % args.group
            return render_template(
                "groups.html",
                sample_to_index=sample_to_index,
                available_samples=available_sample_objects(),
                groups=available_groups(),
                group_samples={g: available_group_samples(group_filename(g))
                               for g in available_groups()},
                message=message,
                error=True)

        elif submit == 'delete':
            if os.path.abspath(args.group).startswith(GROUP_PATH):
                delete_group(os.path.abspath(args.group))
                message = "Deleted group %s" % args.group
                return render_template(
                    "groups.html",
                    sample_to_index=sample_to_index,
                    available_samples=available_sample_objects(),
                    groups=available_groups(),
                    group_samples={
                        g: available_group_samples(group_filename(g))
                        for g in available_groups()
                    },
                    message=message,
                    error=False)

            message = "Could not delete group %s" % args.group
            return render_template(
                "groups.html",
                sample_to_index=sample_to_index,
                available_samples=available_sample_objects(),
                groups=available_groups(),
                group_samples={g: available_group_samples(group_filename(g))
                               for g in available_groups()},
                message=message,
                error=True)
