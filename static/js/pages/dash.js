
/*
* LINE CHART
* ----------
*/
function line_chart()
{
    $.get("dashboard/getAllRecipes", function(data, status)
    {
      alert(data)
      console.log(data)
      var jsonv = JSON.parse(data);       
        var recipesList = [];
        var colors = ['#EF476F','#06D6A0','#118AB2','#073B4C','#3c8dbc','#283618'];
        for (let i = 0; i < jsonv.length; i++) 
        {
            // var array1 = [];
            // var array2 = [];
            // var array3 = [];
            // var array4 = [];
            // var lastarray = [];
            // array1.push(1,parseFloat(jsonv[i].solid));
            // array2.push(2,parseFloat(jsonv[i].dosage1));
            // array3.push(3,parseFloat(jsonv[i].dosage2)); 
            // array4.push(4,parseFloat(jsonv[i].powder)); 
            // lastarray.push(array1);
            // lastarray.push(array2);  
            // lastarray.push(array3);
            // lastarray.push(array4);
            // var title = "Receita " + jsonv[i].id;                                  
            // var line_data1 = {
            //     label: title,
            //     data : lastarray,
            //     color: colors[i]
            // }
            // recipesList.push(line_data1);  
            
            // $.plot('#line-chart', recipesList, {
            //     grid  : {
            //       hoverable  : true,
            //       borderColor: '#f3f3f3',
            //       borderWidth: 1,
            //       tickColor  : '#f3f3f3'
            //     },
            //     series: {
            //       shadowSize: 0,
            //       lines     : {
            //         show: true
            //       },
            //       points    : {
            //         show: true
            //       }
            //     },
            //     lines : {
            //       fill : false,
            //       color: ['#3c8dbc', '#f56954']
            //     },
            //     yaxis : {
            //       show: true
            //     },
            //     xaxis : {
            //       show: true,
            //       ticks: [[1,'Sólido'], [2,'Dosagem 1'], [3,'Dosagem 2'], [4,'Pó']]            
            //     }
            // });
            alert(jsonv[i].solid)
        }

        //Initialize tooltip on hover
        $('<div class="tooltip-inner" id="line-chart-tooltip"></div>').css({
          position: 'absolute',
          display : 'none',
          opacity : 0.8
        }).appendTo('body');

        $('#line-chart').bind('plothover', function (event, pos, item) {

          if (item) {
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2)

            $('#line-chart-tooltip').html(item.series.label + ' of ' + x + ' = ' + y)
              .css({
                top : item.pageY + 5,
                left: item.pageX + 5
              })
              .fadeIn(200)
          } else {
            $('#line-chart-tooltip').hide()
          }

        });
    });
        
}

/*
* BAR CHART
* ----------
*/
// function bar_chart()
// {
//     $.get("/dashboard/getAllReports", function(data, status)
//     {
//         var jsonv = JSON.parse(data);    
//         var newArray = [];
//         for (let i = 0; i < jsonv.length; i++) 
//         {       
//             console.log(jsonv[i]);  
//             var objArray = [jsonv[i].month,jsonv[i].qty];
//             newArray.push(objArray);        
//         }    
//         var bar_data = {
//           data : newArray,
//           bars: { show: true }
//         }

//         $.plot('#bar-chart', [bar_data], {
//           grid  : {
//             borderWidth: 1,
//             borderColor: '#f3f3f3',
//             tickColor  : '#f3f3f3'
//           },
//           series: {
//               bars: {
//               show: true, barWidth: 0.5, align: 'center',
//             },
//           },
//           colors: ['#3c8dbc'],
//           xaxis : {
//             ticks: [[1,'Janeiro'], [2,'Fevereiro'], [3,'Março'], [4,'Abril'], [5,'Maio'], [6,'Junho'],[7,'Julho'], [8,'Agosto'], [9,'Setembro'], [10,'Outubro'], [11,'Novembro'], [12,'Dezembro']]
//           }
//         })

//     });

// }

/*
* DONUT CHART
* ----------
*/
// function donut_chart()
// {
//   var donutData = [
//     {
//       label: 'Sólido',
//       data : 30,
//       color: '#3c8dbc'
//     },
//     {
//       label: 'Pó',
//       data : 20,
//       color: '#0073b7'
//     },
//     {
//       label: 'Dosagem 1',
//       data : 50,
//       color: '#00c0e0'
//     },
//     {
//       label: 'Dosagem 2',
//       data : 20,
//       color: '#00c0eg'
//     }
//   ]
//   $.plot('#donut-chart', donutData, {
//     series: {
//       pie: {
//         show       : true,
//         radius     : 1,
//         innerRadius: 0.5,
//         label      : {
//           show     : true,
//           radius   : 2 / 3,
//           formatter: labelFormatter,
//           threshold: 0.1
//         }

//       }
//     },
//     legend: {
//       show: false
//     }
//   })
// }


 /*
   * Custom Label formatter
   * ----------------------
   */
  function labelFormatter(label, series) {
    return '<div style="font-size:13px; text-align:center; padding:2px; color: #fff; font-weight: 600;">'
      + label
      + '<br>'
      + Math.round(series.percent) + '%</div>'
  }