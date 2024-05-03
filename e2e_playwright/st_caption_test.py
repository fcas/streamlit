# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction


def test_correct_number_of_elements(app: Page):
    caption_containers = app.get_by_test_id("stCaptionContainer")
    expect(caption_containers).to_have_count(8)


def test_correct_content_in_caption(app: Page):
    """Check that the captions have the correct content and also use the correct markdown formatting."""
    caption_containers = app.get_by_test_id("stCaptionContainer")
    expect(caption_containers.nth(1)).to_have_text("This is a caption!")
    expect(caption_containers.nth(2)).to_have_text(
        "This is a caption that contains markdown inside it!"
    )
    expect(caption_containers.nth(3)).to_have_text(
        "This is a caption that contains <div>html</div> inside it!"
    )
    expect(caption_containers.nth(4)).to_have_text(
        "This is a caption that contains html inside it!"
    )
    expect(caption_containers.nth(5)).to_have_text(
        "This is a caption with a help tooltip"
    )
    expect(caption_containers.nth(6)).to_have_text(
        "This is a caption that contains html inside it and a help tooltip!"
    )


def test_match_snapshot(themed_app: Page, assert_snapshot: ImageCompareFunction):
    # fetching the element-container so that when we capture a snapshot, it contains the tooltip
    caption_containers = themed_app.get_by_test_id("element-container").filter(
        has=themed_app.get_by_test_id("stCaptionContainer")
    )
    # nth(0) is sidebar which has its own test method, so start at 1
    assert_snapshot(caption_containers.nth(1), name="st_caption-simple")
    assert_snapshot(caption_containers.nth(2), name="st_caption-with_markdown")
    assert_snapshot(
        caption_containers.nth(3), name="st_caption-with_html_and_unsafe_html_false"
    )
    assert_snapshot(
        caption_containers.nth(4), name="st_caption-with_html_and_unsafe_html_true"
    )
    assert_snapshot(caption_containers.nth(5), name="st_caption-with_tooltip")
    assert_snapshot(caption_containers.nth(6), name="st_caption-with_html_and_tooltip")
    assert_snapshot(
        caption_containers.nth(7), name="st_caption-with_different_markdown_content"
    )


def test_match_snapshot_in_sidebar(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    # expand the sidebar
    themed_app.get_by_test_id("collapsedControl").click()
    sidebar = themed_app.get_by_test_id("stSidebar")
    expect(sidebar).to_be_visible()
    caption_in_sidebar = sidebar.get_by_test_id("stCaptionContainer")
    assert_snapshot(caption_in_sidebar, name="st_caption-sidebar_caption")