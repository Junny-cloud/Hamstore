// Exemple d'ajout d'un bloc HTML personnalisé à la page d'accueil de l'interface d'administration
$(document).ready(function () {
    // Sélectionnez l'élément auquel vous voulez ajouter le bloc HTML personnalisé
    var targetElement = $('.dashboard  #content');

    $.get('pages/test.html', function (data) {
        // Insérez le contenu dans l'élément cible
        targetElement.html(data);
    });
});