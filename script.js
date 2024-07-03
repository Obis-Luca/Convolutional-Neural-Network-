$(document).ready(() => {
  $("#uploadForm").on("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData();
    const imageInput = document.getElementById("imageInput").files[0];
    formData.append("image", imageInput);

    $("#loadingSpinner").show();

    try {
      const response = await $.ajax({
        url: "http://localhost/binaryClassifier/runner.php",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
      });
      const result = JSON.parse(response);
      $("#result").text(result.result);
    } catch (error) {
      console.error("Error uploading image:", error);
    } finally {
      $("#loadingSpinner").hide();
    }
  });
});
