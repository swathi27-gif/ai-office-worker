
from tool_registry import TOOL_REGISTRY, execute_tool


def test_registry_contains_required_tools():
    expected = {
        "find_invoice_files",
        "find_latest_invoice",
        "extract_invoice_details",
        "save_valid_records",
        "verify_saved_records",
    }

    assert expected.issubset(TOOL_REGISTRY.keys())
    print("PASS: All planned actions have registered tools.")


def test_unknown_tool_is_rejected():
    result = execute_tool("delete_everything")

    assert result["success"] is False
    assert result["data"] is None
    assert "Unknown tool" in result["error"]

    print("PASS: Unknown tools are safely rejected.")


def test_invoice_search_tool():
    result = execute_tool("find_invoice_files")

    assert result["success"] is True
    assert isinstance(result["data"], list)
    assert len(result["data"]) >= 1

    print("PASS: Registered invoice search tool works.")


def test_latest_invoice_tool():
    result = execute_tool("find_latest_invoice")

    assert result["success"] is True
    assert isinstance(result["data"], list)
    assert len(result["data"]) == 1

    print("PASS: Latest-invoice tool selects one PDF.")


if __name__ == "__main__":
    test_registry_contains_required_tools()
    test_unknown_tool_is_rejected()
    test_invoice_search_tool()
    test_latest_invoice_tool()

    print("\nAll tool registry tests passed!")
