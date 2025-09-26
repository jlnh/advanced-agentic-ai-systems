# Troubleshooting Guide

## 🛠️ Common Setup Issues and Solutions

### 1. API Key Not Found
```
Error: OpenAI API key not found
```
**Solution**: Ensure `OPENAI_API_KEY` is set in your `.env` file or environment variables.

### 2. Module Import Errors
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**:
- Ensure virtual environment is activated
- Run `pip install -r requirements/base.txt`
- Verify you're using the correct Python interpreter

### 3. Permission Issues
```
PermissionError: [Errno 13] Permission denied
```
**Solution**:
- Ensure proper file permissions
- Check that output directories exist and are writable
- On Windows, run terminal as administrator if needed

### 4. Memory/FAISS Installation Issues
```
Error installing faiss-cpu
```
**Solution**:
```bash
# Try alternative installation
pip install faiss-cpu --no-cache-dir

# Or use conda if available
conda install faiss-cpu -c conda-forge
```

### 5. LangChain Hub Errors
```
Error: Missing LangChain API key
```
**Solution**: Either set `LANGCHAIN_API_KEY` in your `.env` file or use local prompts by setting `use_local_prompt=True` in agent creation.

## 🧪 Testing and Validation

### Running Tests
Each project includes test suites:
```bash
# Run specific project tests
cd code_samples/project_name
python test_*.py

# Or run comprehensive validation
python scripts/test_core_components.py
```

### Validation Checklist
- [ ] Environment setup completed
- [ ] API keys configured
- [ ] Dependencies installed
- [ ] Basic examples run successfully
- [ ] Error handling tested
- [ ] Performance metrics captured

## 🚀 Development Workflow

### Setting Up for Development

1. **Install development dependencies:**
   ```bash
   pip install -r requirements/dev.txt
   ```

2. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

3. **Code formatting:**
   ```bash
   black src/ code_samples/
   flake8 src/ code_samples/
   ```

### Adding New Projects

1. Create project directory under appropriate category
2. Add project-specific requirements to main requirements files
3. Include setup instructions in project README
4. Update this main README with navigation links

## 🔧 Performance and Cost Optimization

### Token Management
- Most examples use `gpt-3.5-turbo` for cost efficiency
- Upgrade to `gpt-4` in config files for better performance
- Monitor token usage with verbose logging

### Caching
- Many projects include caching mechanisms
- Enable caching for repeated operations
- Clear cache regularly to manage disk space

### Rate Limiting
- Built-in rate limiting for external API calls
- Adjust limits based on your API tier
- Implement backoff strategies for production use

## 🛡️ Security Best Practices

- Never commit API keys to version control
- Use `.env` files for configuration (included in `.gitignore`)
- Implement input validation for user inputs
- Restrict file operations to designated directories
- Review and audit external tool integrations