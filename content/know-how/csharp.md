# C# Codesnippets

## Blazor

```csharp
    private ElementReference markdownElement;
    private string renderedHtml = string.Empty;

    [Parameter]
    public string Content { get; set; } = string.Empty;

    private static readonly MarkdownPipeline Pipeline = new MarkdownPipelineBuilder()
        .UseAdvancedExtensions()
        .DisableHtml() // For security, disable raw HTML
        .Build();

    protected override void OnParametersSet()
    {
        if (!string.IsNullOrEmpty(Content))
        {
            renderedHtml = Markdown.ToHtml(Content, Pipeline);
        }
        base.OnParametersSet();
    }

    public void Dispose()
    {
        // Cleanup if needed
    }
```