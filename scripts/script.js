$(document).ready(function() {
    // Ermögliche Drag-and-Drop
    $(document).on('dragstart', '.item', function(e) {
        e.originalEvent.dataTransfer.setData('text/plain', $(this).data('hash'));
        e.originalEvent.dataTransfer.setData('source-chest', $(this).closest('.chest, #unassigned').data('chest-index'));
    });

    $(document).on('dragover', '.chest, #unassigned', function(e) {
        e.preventDefault();
    });

    $(document).on('drop', '.chest, #unassigned', function(e) {
        e.preventDefault();
        var hash = e.originalEvent.dataTransfer.getData('text/plain');
        var sourceChestIndex = e.originalEvent.dataTransfer.getData('source-chest');
        var targetChestIndex = $(this).data('chest-index');

        // Verschiebe das Element im DOM
        var item = $('div.item[data-hash="' + hash + '"]');

        // Aktualisiere Datenattribute
        if (targetChestIndex !== undefined) {
            item.attr('data-chest-index', targetChestIndex);
        } else {
            item.removeAttr('data-chest-index');
        }

        // Füge das Item zum Ziel hinzu
        $(this).find('.items').append(item);

        // Automatisches Speichern
        saveChests();
    });

    // Funktion zum Speichern der Chests
    function saveChests() {
        var chests = [];

        $('.chest').each(function() {
            var chestItems = [];
            $(this).find('.item').each(function() {
                chestItems.push($(this).data('hash'));
            });
            chests.push(chestItems);
        });

        $.ajax({
            url: '/save_chests',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ chests: chests }),
            success: function(response) {
                console.log('Änderungen automatisch gespeichert.');
            },
            error: function() {
                console.error('Fehler beim automatischen Speichern der Änderungen.');
            }
        });
    }

    // Funktionen zum Hinzufügen und Entfernen von Chests
    $('#add-chest-button').click(function() {
        var chestIndex = $('.chest').length;
        var newChest = $('<div class="chest" data-chest-index="' + chestIndex + '">' +
            '<h3>Chest ' + chestIndex + '</h3>' +
            '<div class="items"></div>' +
            '</div>');

        $('#chests').append(newChest);

        // Automatisches Speichern
        saveChests();
    });

    $('#remove-chest-button').click(function() {
        var chestCount = $('.chest').length;
        if (chestCount > 0) {
            var lastChest = $('.chest').last();
            lastChest.find('.item').each(function() {
                $(this).removeAttr('data-chest-index');
                $('#unassigned .items').append($(this));
            });
            lastChest.remove();

            // Aktualisiere die Indizes der Chests
            updateChestIndices();

            // Automatisches Speichern
            saveChests();
        } else {
            alert('Es gibt keine Chests zum Entfernen.');
        }
    });

    // Funktion zum Aktualisieren der Chest-Indizes
    function updateChestIndices() {
        $('.chest').each(function(index) {
            $(this).attr('data-chest-index', index);
            $(this).find('h3').text('Chest ' + index);
        });
    }

    // Initialisiere die Indizes beim Laden der Seite
    updateChestIndices();

    // Optionaler Speichern-Button
    $('#save-button').click(function() {
        saveChests();
        alert('Änderungen gespeichert!');
    });
});
