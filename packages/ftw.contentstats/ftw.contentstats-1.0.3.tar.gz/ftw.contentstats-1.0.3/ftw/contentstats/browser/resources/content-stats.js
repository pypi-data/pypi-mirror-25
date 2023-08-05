
function bindTableHoverEffects(name, chart) {
  var selector = '#content-stats-' + name + ' tr';
  $(selector).on('mouseover', function(event) {
    chart.focus(event.currentTarget.dataset.id);
  });

  $(selector).on('mouseout', function(event) {
    chart.focus();
  });

  $(selector).each(function( index ) {
      var data_id = this.dataset.id;
      d3.select(this).selectAll('td .legend-color')
                     .style('background-color', chart.color(data_id));
  });
}

function createPieChart(name, dataURL) {
  var pie_chart = c3.generate({
    bindto: '#pie-chart-' + name,
    data: {
        url: dataURL,
        mimeType: 'json',
        type : 'pie',
        legend: true
    },
    size: {
        height: 360,
        width: 480
    },
    tooltip: {
        format: {
            value: function (value, ratio, id) {return value;}
        }
    }
  });

  // XXX: Buggy since moving to data.url
  // pie_chart.legend.hide();
  bindTableHoverEffects(name, pie_chart);
}

function createBarChart(name, dataURL) {
  var bar_chart = c3.generate({
    bindto: '#bar-chart-' + name,
    data: {
        url: dataURL,
        mimeType: 'json',
        type : 'bar',
        labels: true,
        legend: true
    },
    tooltip: {
        grouped: false // Default true
    },
    axis: {
        x: {show:false}
    },
    grid: {
        y: {
            show: true
        }
    }
  });

  // XXX: Buggy since moving to data.url
  // bar_chart.legend.hide();
  bindTableHoverEffects(name, bar_chart);
}


$(function() {

  $('.statistic-wrapper').each(function(){
    var wrapper = $(this);
    var infos = wrapper.find('.content-stats-infos');
    var dataURL = infos.data('stat-data-url');
    var name = infos.data('stat-name');

    createPieChart(name, dataURL);
    createBarChart(name, dataURL);
  });

});
