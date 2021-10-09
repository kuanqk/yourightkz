// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
      language: {
        url: "/static/localization/ru.json"
      }
    }
  );
});
