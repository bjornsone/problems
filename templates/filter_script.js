
function update_titles() {
    {% for tag_name in concept_obj['tag_names'] %}
        var title = '{{tag_name}}' + ': ';
        var count = 0;
        var total_count = 0;
        {% set outer_loop = loop %}
        {% for tag_val in concept_obj['tag%d_values' % loop.index0] %}
            if ($("#tag{{outer_loop.index0}}_{{loop.index0}}").is(':checked')) {
                title += '{{tag_val}}, ';
                count ++;
            }
            total_count++;
        {% endfor %}
        if (count==0 || count==total_count) {
            title = '{{tag_name}}' + ': All';
        } else {
            title = title.slice(0, -2);  // Remove the last comma
        }
        $("#tag{{loop.index0}}").text(title);
    {% endfor %}
}

function activate_edit() {
    $("#cancel").show();
    $("#submit").show();
}

function reset_filters() {
    $( 'input[type="checkbox"]' ).prop("checked",false).checkboxradio('refresh');;
    {% for tag, value_list in tag_dict.items() %}
        {% for tag_val in value_list %}
            $("#{{tag}}_{{tag_val}}").prop("checked", true).checkboxradio('refresh');
        {% endfor %}
    {% endfor %}
    update_titles();
    $("#cancel").hide();
    $("#submit").hide();
}

function setup_change_handlers() {
    $( 'input[type="checkbox"]' ).bind( "change", function(event, ui) { update_titles(); activate_edit(); });
    $("#cancel").click(function(event)
    {
        event.preventDefault();
        reset_filters();
    });
}