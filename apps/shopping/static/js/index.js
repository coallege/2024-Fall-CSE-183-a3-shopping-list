"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
const app = Vue.createApp({});


app.data = {
    data: function() {
        return {
            // Complete as you see fit.
        };
    },
    methods: {
        // Complete as you see fit.
        },
};

app.component("shopping-list", {
    setup() {
        
    },
    template: /* html */ `
        <table class="table is-fullwidth is-striped" id="table">
            <tr class="add-row">
                <td class="is-narrow"><i class="is-size-2 fa fa-plus-square has-text-success add-item"></i></td>
                <td><input class="input add-item" type="text" name="new_item"></td>
                <td class="is-narrow"></td>
            </tr>
            <template v-for="product in cart">
                <product
                    @click="cellClick(row, col)"
                    :status="cellStatus(row, col)"
                    :winning="cellWinning(row, col)"
                ></product>
            </template>
        </table>
    `
})

app.component("product", {
    props: ["id", "name", "checked"],
    setup() {
        return {
            updateCheckState,
            
        };
    },
    template: /* html */ `
        <tr class="item-row">
            <td class="check is-narrow">
                <input type="checkbox" :checked={checked} @change>
            </td>
            <td class="item">{name}</td>
            <td class="trash is-narrow">
                <i class="trash has-text-danger fa fa-trash"></i>
            </td>
        </tr>
    `,
});


app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    // Complete.
}

// This is the initial data load.
app.load_data();

