import {searchApiResultDataciteTemplate} from "./templates"

export class DataciteSearcher {

    constructor(importer) {
        this.importer = importer
    }

    bind() {
        let that = this
        jQuery('#bibimport-search-result-datacite .api-import').on('click', function() {
            let doi = jQuery(this).attr('data-doi')
            that.getBibtex(doi)
        })
    }

    lookup(searchTerm) {

        return new Promise(resolve => {
            jQuery.ajax({
                data: {
                    'query': searchTerm
                },
                dataType: "json",
                url: 'https://api.datacite.org/works?/select',
                success: result => {
                    let items = result['data']
                    jQuery("#bibimport-search-result-datacite").empty()
                    if (items.length) {
                        jQuery("#bibimport-search-result-datacite").html('<h3>Datacite</h3>')
                    }
                    jQuery('#bibimport-search-result-datacite').append(
                        searchApiResultDataciteTemplate({items})
                    )
                    this.bind()
                    resolve()
                }
            })
        })
    }

    getBibtex(doi) {
        doi = encodeURIComponent(doi)
        jQuery.ajax({
            dataType: 'text',
            method: 'GET',
            url: `https://data.datacite.org/application/x-bibtex/${doi}`,
            success: response => {
                this.importer.importBibtex(response)
            }

        })
    }

}
