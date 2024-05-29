import { test, expect, jest, beforeAll } from "@jest/globals"
import jsdom from "jsdom"

let dom = new jsdom.JSDOM(`
<div id="dialog-confirm" title="Delete your post?">
  <p>This cannot be undone.</p>
</div>
<button class="pure-button" id="delete-post"><i class="fa fa-solid fa-times"></i></button>
<label for="editing-see-guesses" class="pure-checkbox">
  <input type="checkbox" id="editing-see-guesses" name="see-guesses"/> Users can see other people's guesses. 
</label>
`)
let window = dom.window
let $ = require("jquery")(window)

/**
 * @type string
 */
var username = "test@example.com";

/**
 * 
 * @param {boolean} show_comment 
 */
function setup(show_comment) {
  $("#dialog-confirm").hide();
  $('#editing-see-guesses').prop('checked', show_comment);
}

beforeAll(() => setup(false))
test("dialog-confirm hidden", () => {
  expect($("#dialog-confirm").css("display")).toBe("none")
})
test("editing-see-guesses", () => {
  expect($("#editing-see-guesses").prop("checked")).toBe(false)
})
test("editing-see-guesses, show_comment=true", () => {
  setup(true)
  expect($("#editing-see-guesses").prop("checked")).toBe(true)
})