/**
 * Fetch the books data from api,
 * then visualize the data.
 * @param {Array} k intended number of top rating books
 */
function getBooks(k) {
    fetch('http://127.0.0.1:5000/api/search?q=book.book_id:', {
        method: 'GET'
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log(data)
        if (data instanceof Array) {
            dataset = parseData(data, k)
            visualize(dataset)
        }
    })
    .catch(error => {
        console.log(error)
    })
}

/**
 * Parse the data to retrive only book id and rating,
 * then sort the data in descending order of rating.
 * @param {Array} data array of book dictionary
 * @param {Integer} k intended number of top rating books
 * @returns sorted array of book dictionary
 */
function parseData(data, k) {
    var dataset = []
    var targetK = k
    if (data.length < k) {
        targetK = data.length
    }
    for (var i = 0; i < data.length; i++) {
        doc = data[i]
        if ('rating' in doc) {
            dataset.push({'book_id': doc['book_id'], 'rating': doc['rating']})
        }
    }
    sortedDataset = quicksort(dataset).reverse()
    if (sortedDataset.length < targetK) {
        return sortedDataset
    }
    return sortedDataset.slice(0, targetK)
}

/**
 * Quicksort for array of book dictionary
 * @param {Array} array array of book dictionary to sort
 * @returns sorted array
 */
function quicksort(array) {
    if (array.length <= 1) {
        return array
    }
    var left = []
    var right = []
    var pivot = array[0]
    var pivotVal = Number(pivot['rating'])
    for (var i = 1; i < array.length; i++) {
        Number(array[i]['rating']) < pivotVal ? left.push(array[i]) : right.push(array[i])
    }
    return quicksort(left).concat(pivot, quicksort(right))
}

/**
 * Use bar chart in svg to visualize the top rating books
 * @param {Array} dataset array of book dictionary
 */
function visualize(dataset) {
    var xLabels = []
    for (var i = 0; i < dataset.length; i++) {
        xLabels.push(dataset[i]['book_id'])
    }

    d3.select('svg').remove()
    d3.select('p').append('svg')
    d3.select('h3').text('Top ' + dataset.length + ' Rating Books (y: rating, x: id)')

    var svgWidth = 1000
    var svgHeight = 500
    var yAxisPosX = 30
    var xAxisBarGap = svgHeight * 0.1
    var barWidth = (svgWidth - yAxisPosX - 5) / dataset.length
    var barPadding = barWidth * 0.2

    var svg = d3.select('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)

    var yScale = d3.scaleLinear()
        .domain([0, 5.0])
        .range([0, svgHeight * 0.8])

    var barChart = svg.selectAll('rect')
        .data(dataset)
        .enter()
        .append('rect')
        .attr('y', function(d) {
            return svgHeight - xAxisBarGap - yScale(d['rating'])
        })
        .attr('height', function(d) {
            return yScale(d['rating'])
        })
        .attr('width', barWidth - barPadding)
        .attr('transform', function(d, i) {
            var translate = [barWidth * i + yAxisPosX + 5, 0]
            return 'translate(' + translate + ')'
        })

    var text = svg.selectAll('text')
        .data(dataset)
        .enter()
        .append('text')
        .text(function(d) {
            return d['rating']
        })
        .attr('y', function(d, i) {
            return svgHeight * 0.9 - yScale(d['rating']) - 2
        })
        .attr('x', function(d, i) {
            return barWidth * i + barWidth * 0.2 + yAxisPosX
        })
        .attr('fill', '#A64C38')

    // Axes
    var yAxisScale = d3.scaleLinear()
        .domain([0, 5.0])
        .range([svgHeight * 0.8, 0])

    var yAxis = d3.axisLeft()
        .scale(yAxisScale)

    svg.append('g')
        .attr('transform', 'translate(' + yAxisPosX + ',' + svgHeight * 0.1 + ')')
        .call(yAxis)

    var xAxisScale = d3.scalePoint()
        .domain(xLabels)
        .range([yAxisPosX, svgWidth - yAxisPosX - barWidth * 0.5])

    var xAxis = d3.axisBottom()
        .scale(xAxisScale)
        .ticks(xLabels.length)

    var xAxisGroup = svg.append('g')
        .attr('transform', 'translate(' + yAxisPosX + ',' + svgHeight * 0.9 + ')')
        .call(xAxis)

    xAxisGroup.selectAll('text')
        .attr('transform', 'translate(0, 10) rotate(-20)')
}

const button = document.getElementById('build-button')
const inputK = document.getElementById('input-k')
button.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    getBooks(inputK.value)
})
