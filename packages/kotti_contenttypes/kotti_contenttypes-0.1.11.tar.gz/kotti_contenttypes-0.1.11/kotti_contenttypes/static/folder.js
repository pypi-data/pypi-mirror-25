$(document).ready(function(){
  var options = {
      valueNames: [ 'title', 'description', 'contenttype'],
      page: 25,
      plugins: [
        ListPagination({})
      ]
    };

    var listObj = new List('folder-listing', options);
});
