import {setCheckableLabel} from "../../common"
import {BibLatexApiImporter} from "../../citation-api-import"

export class BibLatexApiImporterCitationDialog {
    constructor(citationDialog) {
        this.citationDialog = citationDialog
    }

    init() {
        this.addButton()
    }

    addButton() {
        this.citationDialog.buttons.unshift({
            text: gettext('Import from database'),
            click: () => {
                this.initImporter()
            },
            class: 'fw-button fw-light fw-add-button'
        })
    }

    initImporter() {
        //import via web api
        let apiImporter = new BibLatexApiImporter(
            this.citationDialog.editor.mod.db.bibDB,
            bibEntries => {
                this.citationDialog.addToCitableItems(bibEntries)
                jQuery('.fw-checkable').unbind('click')
                jQuery('.fw-checkable').bind('click', function() {
                    setCheckableLabel(jQuery(this))
                })
            }
        )

        apiImporter.init()
    }
}
