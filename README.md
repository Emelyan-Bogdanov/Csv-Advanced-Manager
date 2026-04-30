# Csv-Advanced-Manager
A system to manage csv files without having knowledge about programming , it does most csv pandas  functionnalities , such as cleaning data   , select rows/columns and split data , also +20 other advanced useful feautures , it contains two parts : 1. CSV Manager 2. VisualiseCsv


___________________

# 📊 DataVault: No-Code CSV Management & Analysis Platform

## Table of Contents
1. [Platform Overview](#platform-overview)
2. [Architecture](#architecture)
3. [Part 1: CSV Management Panel](#part-1-csv-management-panel)
4. [Part 2: Data Visualization & Analytics](#part-2-data-visualization--analytics)
5. [Feature List](#complete-feature-list)
6. [Technical Stack](#technical-stack)
7. [Installation & Setup](#installation--setup)
8. [User Guide](#user-guide)
9. [API Endpoints](#api-endpoints)
10. [Database Schema](#database-schema)

---

## Platform Overview

**DataVault** is an enterprise-grade, no-code platform designed for non-technical users to manage, clean, visualize, and analyze CSV files without programming knowledge. It empowers business analysts, data entry operators, and managers to perform advanced data operations through an intuitive graphical interface.

### Key Vision
- **Non-technical users first**: Zero Python/SQL knowledge required
- **Drag-and-drop simplicity**: Intuitive UI for complex operations
- **Enterprise features**: Professional data handling, validation, and security
- **Two-part architecture**: Data manipulation (Part 1) + Analytics (Part 2)

### Target Users
- Business analysts performing data cleaning
- Marketing teams managing customer lists
- HR departments handling employee records
- Sales teams maintaining pipeline data
- Researchers preparing datasets for analysis
- Any non-technical user managing tabular data

---

## Architecture

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        DataVault Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Frontend (React + Tailwind)                │    │
│  │                                                           │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │    Part 1: CSV Management Panel                 │   │    │
│  │  │  - Upload & File Explorer                       │   │    │
│  │  │  - Data Cleaning Tools                          │   │    │
│  │  │  - Column/Row Operations                        │   │    │
│  │  │  - Data Transformation                          │   │    │
│  │  │  - Export & Save                                │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                           │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │  Part 2: Analytics & Visualization Dashboard    │   │    │
│  │  │  - Interactive Charts                           │   │    │
│  │  │  - Statistical Analysis                         │   │    │
│  │  │  - Data Profiling                               │   │    │
│  │  │  - Descriptive Statistics                       │   │    │
│  │  │  - Custom Reports                               │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↕                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         Backend (Flask/FastAPI + Python)               │    │
│  │                                                           │    │
│  │  - REST API Layer                                        │    │
│  │  - Pandas Data Processing Engine                         │    │
│  │  - File Management Service                              │    │
│  │  - Data Cleaning & Transformation Module                │    │
│  │  - Analytics & Statistics Engine                         │    │
│  │  - User Authentication & Authorization                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              ↕                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         Data Layer (PostgreSQL + File Storage)          │    │
│  │                                                           │    │
│  │  - User metadata & project information                   │    │
│  │  - Processing history & audit logs                       │    │
│  │  - Saved configurations & templates                      │    │
│  │  - CSV files (local storage / cloud storage)            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Upload → File Validation → Pandas Processing → Database Storage
                                        ↓
                              Real-time Preview
                                        ↓
                    Data Cleaning/Transformation Operations
                                        ↓
                    Analytical Operations & Visualizations
                                        ↓
                    Export / Save to Database
```

---

## Part 1: CSV Management Panel

The **CSV Management Panel** is the core data manipulation engine. It allows users to perform complex data operations through a visual interface without writing code.

### 1.1 File Management

#### Features
- **Upload CSV Files**: Drag-and-drop or click to upload
  - File size limit: Up to 500MB (configurable)
  - Supported formats: CSV, TSV, Excel (.xlsx)
  - Automatic encoding detection (UTF-8, Latin-1, etc.)

- **File Browser & Organization**
  - View all uploaded files with metadata (size, upload date, rows/columns)
  - Search files by name
  - Folder/project organization
  - Preview first 10 rows instantly
  - File versioning (keep history of changes)

- **File Operations**
  - Duplicate/Copy files
  - Rename files
  - Delete files (with confirmation)
  - Download original file
  - View file statistics (size, dimensions, encoding)

#### Implementation
```python
# Backend Example
@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    encoding = chardet.detect(file.read())['encoding']
    df = pd.read_csv(file, encoding=encoding)
    # Save to database with metadata
    return {'file_id': file_id, 'rows': len(df), 'columns': len(df.columns)}
```

---

### 1.2 Data Cleaning Operations

#### 1.2.1 Handle Missing Values (Nulls)
Users can:
- **View missing data**: Show percentage of nulls per column
- **Delete rows with nulls**: Remove rows containing any/all null values
- **Delete columns with nulls**: Remove columns with > X% missing
- **Fill missing values**:
  - Fill with constant: `0`, `'Unknown'`, etc.
  - Fill with mean/median (numeric columns)
  - Fill with mode (categorical)
  - Forward fill / backward fill (time-series)
  - Interpolation (linear, polynomial)
- **Detect patterns**: Which rows/columns have nulls?

```python
# Backend Example
@app.route('/api/operations/handle_missing', methods=['POST'])
def handle_missing():
    operation = request.json['operation']
    column = request.json['column']
    
    if operation == 'drop_rows':
        df = df.dropna()
    elif operation == 'drop_columns':
        df = df.dropna(axis=1)
    elif operation == 'fill_mean':
        df[column] = df[column].fillna(df[column].mean())
    elif operation == 'fill_forward':
        df[column] = df[column].fillna(method='ffill')
    
    return {'success': True, 'rows': len(df)}
```

#### 1.2.2 Data Type Cleaning
- **Auto-detect column types**: Suggests data types based on content
- **Convert data types**: String → Int, Float, Date, Boolean
- **Fix type mismatches**:
  - Detect columns that should be numeric but contain text
  - Suggest corrections
  - Handle currency symbols ($100 → 100)
  - Parse dates in multiple formats

```python
@app.route('/api/operations/convert_type', methods=['POST'])
def convert_type():
    column = request.json['column']
    target_type = request.json['target_type']  # 'int', 'float', 'date', 'bool'
    
    if target_type == 'numeric':
        df[column] = pd.to_numeric(df[column], errors='coerce')
    elif target_type == 'datetime':
        df[column] = pd.to_datetime(df[column], format='infer')
    elif target_type == 'boolean':
        df[column] = df[column].astype(bool)
    
    return {'success': True, 'invalid_count': df[column].isna().sum()}
```

#### 1.2.3 Remove Special Characters & Whitespace
- **Trim whitespace**: Remove leading/trailing spaces
- **Remove special characters**: 
  - Keep only alphanumeric
  - Remove punctuation
  - Remove HTML tags
  - Normalize Unicode
- **Case conversion**: Uppercase, lowercase, title case
- **Replace substrings**: Find and replace (with regex support for advanced users)

```python
@app.route('/api/operations/clean_text', methods=['POST'])
def clean_text():
    column = request.json['column']
    operation = request.json['operation']
    
    if operation == 'trim':
        df[column] = df[column].str.strip()
    elif operation == 'remove_special':
        df[column] = df[column].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
    elif operation == 'uppercase':
        df[column] = df[column].str.upper()
    elif operation == 'remove_html':
        df[column] = df[column].str.replace(r'<[^>]+>', '', regex=True)
    
    return {'success': True}
```

#### 1.2.4 Duplicate Removal
- **Identify duplicates**: Show all duplicate rows
- **Remove exact duplicates**: Keep first/last occurrence
- **Remove duplicates by column subset**: Remove duplicates based on specific columns
- **Fuzzy matching**: Remove near-duplicates (e.g., "John Smith" vs "Jon Smith")

```python
@app.route('/api/operations/remove_duplicates', methods=['POST'])
def remove_duplicates():
    subset = request.json.get('subset')  # columns to check
    keep = request.json.get('keep', 'first')  # 'first', 'last', False
    
    duplicates_count = df.duplicated(subset=subset).sum()
    df = df.drop_duplicates(subset=subset, keep=keep)
    
    return {'duplicates_removed': duplicates_count, 'remaining_rows': len(df)}
```

#### 1.2.5 Outlier Detection & Handling
- **Detect outliers**: Statistical methods (Z-score, IQR)
- **Visualize outliers**: Highlight in data preview
- **Remove outliers**: Delete rows with outlier values
- **Cap outliers**: Replace with min/max threshold values

```python
@app.route('/api/operations/handle_outliers', methods=['POST'])
def handle_outliers():
    column = request.json['column']
    method = request.json['method']  # 'zscore', 'iqr'
    
    if method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers = z_scores > 3
    elif method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        outliers = (df[column] < Q1 - 1.5*IQR) | (df[column] > Q3 + 1.5*IQR)
    
    return {'outliers_found': outliers.sum(), 'outlier_rows': outliers.tolist()}
```

---

### 1.3 Row & Column Operations

#### 1.3.1 Select/Filter Rows
- **Simple filters**: 
  - Column == value
  - Column > / < / >= / <= value
  - Column contains text
  - Column is empty
  - Column starts/ends with text

- **Complex filters** (AND/OR logic):
  - Multiple conditions: "(Age > 25) AND (City == 'Casablanca')"
  - Regular expressions: "Email matches pattern"

- **Row range selection**: Keep rows 100-500, delete rest

```python
@app.route('/api/operations/filter_rows', methods=['POST'])
def filter_rows():
    filters = request.json['filters']  # [{'column': 'age', 'operator': '>', 'value': 25}]
    
    mask = pd.Series(True, index=df.index)
    for f in filters:
        col, op, val = f['column'], f['operator'], f['value']
        if op == '==':
            mask &= (df[col] == val)
        elif op == '>':
            mask &= (df[col] > val)
        # ... more operators
    
    return {'filtered_rows': mask.sum()}
```

#### 1.3.2 Select/Filter Columns
- **Select specific columns**: Choose columns to keep
- **Drop columns**: Remove unwanted columns
- **Rename columns**: Bulk rename or individual
- **Reorder columns**: Drag-and-drop column ordering
- **Select by pattern**: Keep columns matching "customer_*" pattern

```python
@app.route('/api/operations/select_columns', methods=['POST'])
def select_columns():
    selected = request.json['columns']  # list of column names
    df = df[selected]
    return {'selected_columns': len(selected), 'total_columns': len(df.columns)}
```

#### 1.3.3 Split Data
- **Split by row count**: 
  - Training (80%) / Test (20%) split
  - Custom percentages
  
- **Split by condition**: 
  - Split based on column value
  - Create separate files for each category

- **Random sampling**:
  - Sample X rows randomly
  - Stratified sampling by category

- **Time-based split**: Split by date range

```python
@app.route('/api/operations/split_data', methods=['POST'])
def split_data():
    method = request.json['method']  # 'percentage', 'condition', 'random'
    
    if method == 'percentage':
        train_pct = request.json['train_pct']
        split_index = int(len(df) * train_pct / 100)
        train_df = df[:split_index]
        test_df = df[split_index:]
    
    elif method == 'condition':
        column = request.json['column']
        value = request.json['value']
        df1 = df[df[column] == value]
        df2 = df[df[column] != value]
    
    elif method == 'random':
        frac = request.json['sample_pct'] / 100
        df1 = df.sample(frac=frac)
        df2 = df.drop(df1.index)
    
    return {'dataset1_rows': len(df1), 'dataset2_rows': len(df2)}
```

---

### 1.4 Data Transformation

#### 1.4.1 Text Operations
- **Concatenate columns**: Combine "First_Name" + "Last_Name" → "Full_Name"
- **Extract substring**: Extract area code from phone number
- **Split column**: Split "Full_Name" → "First_Name" + "Last_Name"
- **Replace text**: Global find and replace with optional regex
- **Format numbers**: Add thousand separators, decimal places

```python
@app.route('/api/operations/text_transform', methods=['POST'])
def text_transform():
    operation = request.json['operation']
    
    if operation == 'concatenate':
        cols = request.json['columns']
        separator = request.json.get('separator', ' ')
        df['new_col'] = df[cols].agg(separator.join, axis=1)
    
    elif operation == 'extract':
        column = request.json['column']
        pattern = request.json['pattern']  # regex
        df['extracted'] = df[column].str.extract(pattern)
    
    elif operation == 'split':
        column = request.json['column']
        separator = request.json['separator']
        new_cols = df[column].str.split(separator, expand=True)
        df[['col1', 'col2']] = new_cols
    
    return {'success': True}
```

#### 1.4.2 Numeric Operations
- **Math operations**: Add, subtract, multiply, divide columns
- **Rounding**: Round to specific decimal places
- **Normalize/Scale**: Min-max scaling (0-1) or standardization
- **Binning**: Convert continuous to categorical (age → age groups)
- **Percentage change**: Calculate % change between rows

```python
@app.route('/api/operations/numeric_transform', methods=['POST'])
def numeric_transform():
    operation = request.json['operation']
    columns = request.json['columns']
    
    if operation == 'add':
        df['result'] = df[columns[0]] + df[columns[1]]
    elif operation == 'normalize':
        col = columns[0]
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    elif operation == 'binning':
        col = columns[0]
        bins = request.json['bins']
        labels = request.json['labels']
        df[col + '_binned'] = pd.cut(df[col], bins=bins, labels=labels)
    
    return {'success': True}
```

#### 1.4.3 Date/Time Operations
- **Parse dates**: Auto-detect and convert to datetime
- **Extract components**: Year, month, day, quarter from dates
- **Calculate age**: From birth date to today
- **Date arithmetic**: Add/subtract days, calculate duration
- **Format dates**: Change display format (YYYY-MM-DD vs DD/MM/YYYY)

```python
@app.route('/api/operations/date_transform', methods=['POST'])
def date_transform():
    column = request.json['column']
    operation = request.json['operation']
    
    df[column] = pd.to_datetime(df[column])
    
    if operation == 'extract_year':
        df[column + '_year'] = df[column].dt.year
    elif operation == 'extract_month':
        df[column + '_month'] = df[column].dt.month
    elif operation == 'age':
        df['age'] = (pd.Timestamp.now() - df[column]).dt.days // 365
    elif operation == 'duration':
        col2 = request.json['end_column']
        df['duration_days'] = (df[col2] - df[column]).dt.days
    
    return {'success': True}
```

#### 1.4.4 Categorical Operations
- **Create categories**: Define custom categories/groups
- **Map values**: Map old values to new values (1→'Yes', 0→'No')
- **One-hot encoding**: Convert categories to binary columns
- **Frequency analysis**: Show value counts

```python
@app.route('/api/operations/categorical_transform', methods=['POST'])
def categorical_transform():
    column = request.json['column']
    operation = request.json['operation']
    
    if operation == 'map':
        mapping = request.json['mapping']  # {'old': 'new', ...}
        df[column] = df[column].map(mapping)
    
    elif operation == 'one_hot':
        encoded = pd.get_dummies(df[column], prefix=column)
        df = pd.concat([df, encoded], axis=1)
    
    elif operation == 'frequency':
        counts = df[column].value_counts()
        return {'frequencies': counts.to_dict()}
    
    return {'success': True}
```

---

### 1.5 Advanced Features

#### 1.5.1 Data Validation Rules
- **Create validation rules**: Define what "clean" data looks like
  - Email format validation
  - Phone number format
  - Numeric range checks (age 0-120)
  - Pattern matching
- **Check data**: Run validation and show violations
- **Auto-fix**: Attempt to fix common issues

#### 1.5.2 Merge/Join Operations
- **Combine files**: Merge two CSV files by common column
- **Join types**: Inner, left, right, full outer join
- **Concatenate files**: Stack files on top of each other

```python
@app.route('/api/operations/merge', methods=['POST'])
def merge_files():
    file1_id = request.json['file1_id']
    file2_id = request.json['file2_id']
    join_column = request.json['join_column']
    join_type = request.json['join_type']  # 'inner', 'left', 'right', 'outer'
    
    df1 = load_file(file1_id)
    df2 = load_file(file2_id)
    
    merged = pd.merge(df1, df2, on=join_column, how=join_type)
    
    return {'merged_rows': len(merged), 'merged_columns': len(merged.columns)}
```

#### 1.5.3 Pivot Tables
- **Create pivot tables**: Summarize data by grouping
- **Aggregation options**: Sum, count, average, min, max
- **Export pivot table**: Save as new CSV

```python
@app.route('/api/operations/pivot', methods=['POST'])
def create_pivot():
    index_col = request.json['index']
    columns_col = request.json['columns']
    values_col = request.json['values']
    aggfunc = request.json['aggfunc']  # 'sum', 'mean', 'count', etc.
    
    pivot = df.pivot_table(
        index=index_col,
        columns=columns_col,
        values=values_col,
        aggfunc=aggfunc
    )
    
    return {'pivot_shape': pivot.shape}
```

#### 1.5.4 Grouping & Aggregation
- **Group by column**: Group data by category
- **Calculate aggregates**: Count, sum, average per group
- **Multi-level grouping**: Group by 2+ columns

```python
@app.route('/api/operations/groupby', methods=['POST'])
def groupby_operation():
    group_cols = request.json['group_by']
    agg_specs = request.json['aggregations']  # {'revenue': 'sum', 'count': 'count'}
    
    grouped = df.groupby(group_cols).agg(agg_specs)
    
    return {'groups': len(grouped)}
```

#### 1.5.5 Sorting & Ranking
- **Sort by column**: Ascending or descending
- **Multi-column sort**: Sort by primary, then secondary column
- **Rank rows**: Assign rank based on column values
- **Top/Bottom N**: Keep top 100 rows by value

```python
@app.route('/api/operations/sort', methods=['POST'])
def sort_data():
    sort_by = request.json['sort_by']  # [('revenue', 'desc'), ('date', 'asc')]
    
    for col, direction in reversed(sort_by):
        df = df.sort_values(by=col, ascending=(direction == 'asc'))
    
    return {'success': True}
```

#### 1.5.6 Undo/Redo & History
- **Operation history**: View all operations performed
- **Undo/Redo**: Revert or reapply last N operations
- **Save checkpoints**: Create restore points

---

### 1.6 Export & Save

#### Export Options
- **Download CSV**: Export cleaned data as CSV
- **Export Excel**: Export as .xlsx with formatting
- **Export to Database**: Save to PostgreSQL/MySQL table
- **Email CSV**: Send file via email
- **Schedule exports**: Auto-export on schedule

#### Save Features
- **Save to project**: Keep processed file in platform
- **Version control**: Keep multiple versions
- **Save as template**: Save cleaning steps for reuse

```python
@app.route('/api/operations/export', methods=['POST'])
def export_data():
    format = request.json['format']  # 'csv', 'excel', 'json'
    
    if format == 'csv':
        csv_file = df.to_csv(index=False)
        return send_file(csv_file, mimetype='text/csv')
    elif format == 'excel':
        excel_file = df.to_excel(index=False)
        return send_file(excel_file, mimetype='application/vnd.ms-excel')
    elif format == 'json':
        return df.to_json()
```

---

## Part 2: Data Visualization & Analytics

The **Analytics Dashboard** transforms raw data into actionable insights through interactive visualizations and statistical analysis.

### 2.1 Data Profiling

#### Column Statistics
For each column, automatically generate:
- **Data type**: String, Integer, Float, Boolean, Date
- **Non-null count**: How many non-empty values
- **Null percentage**: What % of data is missing
- **Unique values**: How many distinct values
- **Cardinality**: Low, medium, high

#### Numeric Columns
- **Min, Max, Mean, Median**: Central tendency and range
- **Standard deviation**: Measure of spread
- **Quartiles**: Q1, Q2 (median), Q3 for distribution shape
- **Skewness**: Is distribution symmetric?
- **Kurtosis**: Tails of distribution

#### Categorical Columns
- **Mode**: Most frequent value
- **Value frequency**: Count of each category
- **Diversity**: How many categories?
- **Top values**: Pie chart of top 5 categories

#### Text Columns
- **Avg length**: Average text length
- **Min/Max length**: Range of lengths
- **Unique values**: How many different texts
- **Common patterns**: Detect emails, phone numbers, URLs

```python
@app.route('/api/analytics/profile/<file_id>')
def profile_data(file_id):
    df = load_file(file_id)
    
    profile = {}
    for col in df.columns:
        profile[col] = {
            'dtype': str(df[col].dtype),
            'non_null': df[col].notna().sum(),
            'null_pct': (df[col].isna().sum() / len(df)) * 100,
            'unique': df[col].nunique(),
        }
        
        if df[col].dtype in ['int64', 'float64']:
            profile[col].update({
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
            })
        else:
            profile[col]['mode'] = df[col].mode()[0]
            profile[col]['value_counts'] = df[col].value_counts().head(10).to_dict()
    
    return profile
```

---

### 2.2 Interactive Charts & Visualizations

#### Chart Types Available

**1. Bar Charts**
- Horizontal or vertical bars
- Show frequency counts or aggregated values
- Perfect for categorical comparisons
- Example: Sales by region

**2. Pie Charts**
- Show composition/breakdown
- Percentage labels
- Example: Market share by competitor

**3. Line Charts**
- Show trends over time
- Multiple lines for comparison
- Ideal for time-series
- Example: Revenue over months

**4. Histogram**
- Show distribution of numeric data
- Customizable bins
- Bell curves for normal distribution
- Example: Age distribution

**5. Scatter Plot**
- Show relationship between two numeric variables
- Color by third variable
- Size by fourth variable
- Identify clusters and outliers
- Example: Price vs Performance

**6. Box Plot**
- Show distribution quartiles and outliers
- Compare distributions across groups
- Example: Salary by department

**7. Heatmap**
- Show correlation between variables
- Color intensity indicates strength
- Example: Correlation matrix

**8. Area Chart**
- Stacked or unstacked
- Show cumulative values
- Example: Revenue breakdown by product

**9. Violin Plot**
- Show distribution density
- Compare across categories
- Example: Customer value by segment

```python
@app.route('/api/charts/create', methods=['POST'])
def create_chart():
    chart_type = request.json['chart_type']
    x_col = request.json.get('x_col')
    y_col = request.json.get('y_col')
    group_col = request.json.get('group_col')
    
    df = load_file(request.json['file_id'])
    
    if chart_type == 'bar':
        chart = df.groupby(x_col)[y_col].sum().plot(kind='bar')
    elif chart_type == 'scatter':
        chart = df.plot.scatter(x=x_col, y=y_col, c=group_col, cmap='viridis')
    elif chart_type == 'histogram':
        chart = df[x_col].plot(kind='hist', bins=30)
    elif chart_type == 'pie':
        chart = df[x_col].value_counts().plot(kind='pie')
    elif chart_type == 'line':
        chart = df.plot(x=x_col, y=y_col, kind='line')
    
    # Convert to JSON/HTML for frontend
    return chart_to_json(chart)
```

---

### 2.3 Statistical Analysis

#### Correlation Analysis
- **Pearson correlation**: Measure linear relationship
- **Spearman correlation**: Measure monotonic relationship
- **Correlation matrix**: All variable pairs
- **Heatmap visualization**: Color-coded strength

```python
@app.route('/api/analytics/correlation', methods=['POST'])
def correlation_analysis():
    file_id = request.json['file_id']
    method = request.json.get('method', 'pearson')
    
    df = load_file(file_id)
    numeric_df = df.select_dtypes(include=[np.number])
    
    corr_matrix = numeric_df.corr(method=method)
    
    return {
        'correlation_matrix': corr_matrix.to_dict(),
        'highest_correlations': find_top_correlations(corr_matrix, n=10)
    }
```

#### Distribution Analysis
- **Normality tests**: Shapiro-Wilk, Anderson-Darling
- **Distribution shape**: Histogram with normal curve overlay
- **Q-Q plots**: Compare to normal distribution
- **Identify distribution type**: Normal, skewed, bimodal, etc.

#### Outlier Analysis
- **Statistical methods**: Z-score, IQR, Isolation Forest
- **Visualize outliers**: In charts with highlighting
- **Outlier report**: Details about each outlier
- **Impact assessment**: How outliers affect statistics

```python
@app.route('/api/analytics/outliers', methods=['POST'])
def outlier_analysis():
    file_id = request.json['file_id']
    column = request.json['column']
    method = request.json.get('method', 'iqr')
    
    df = load_file(file_id)
    
    if method == 'iqr':
        Q1, Q3 = df[column].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = (df[column] < lower) | (df[column] > upper)
    
    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outliers = z_scores > 3
    
    return {
        'outlier_count': outliers.sum(),
        'outlier_percentage': (outliers.sum() / len(df)) * 100,
        'outlier_values': df.loc[outliers, column].tolist()
    }
```

---

### 2.4 Descriptive Statistics & Summaries

#### Auto-Generated Report
System automatically generates insights:
- "The dataset contains X rows and Y columns"
- "Average customer lifetime value is $2,500"
- "75% of customers are in the 25-45 age range"
- "There's a strong correlation (r=0.89) between spending and customer tenure"
- "Revenue increased 15% month-over-month"

#### Custom Summaries
Users can create custom summaries:
- Select metrics to highlight
- Define thresholds for "good" vs "concerning" values
- Generate executive summaries

```python
@app.route('/api/analytics/summary', methods=['POST'])
def generate_summary():
    file_id = request.json['file_id']
    df = load_file(file_id)
    
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'null_percentage': (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100,
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
    }
    
    # Add column-specific insights
    for col in df.select_dtypes(include=[np.number]).columns:
        summary[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'range': f"{df[col].min()} - {df[col].max()}"
        }
    
    return summary
```

---

### 2.5 Data Segmentation & Grouping

#### Segment Analysis
- **Create segments**: Divide data into groups (High/Medium/Low value customers)
- **Segment metrics**: Statistics per segment
- **Segment comparison**: Side-by-side comparison
- **Segment profiles**: Characteristics of each segment

#### Cohort Analysis
- **Cohort definition**: Group by signup date, product, region, etc.
- **Cohort metrics**: Trends within each cohort
- **Retention curves**: How cohorts behave over time
- **Churn analysis**: Which cohorts churn most?

```python
@app.route('/api/analytics/segments', methods=['POST'])
def segment_analysis():
    file_id = request.json['file_id']
    segment_col = request.json['segment_column']
    metric_col = request.json['metric_column']
    
    df = load_file(file_id)
    
    segments = df.groupby(segment_col)[metric_col].agg([
        'count', 'sum', 'mean', 'median', 'std', 'min', 'max'
    ]).to_dict()
    
    return {'segments': segments}
```

---

### 2.6 Trend Analysis

#### Time-Series Decomposition
- **Trend**: Overall direction
- **Seasonality**: Repeating patterns
- **Residuals**: Unexplained variation
- **Forecast**: Predict next period

#### Growth Metrics
- **Month-over-month growth**: % change month to month
- **Year-over-year growth**: Compare to same period last year
- **Cumulative growth**: Running total
- **Compound annual growth rate (CAGR)**: Average annual growth

```python
@app.route('/api/analytics/trends', methods=['POST'])
def trend_analysis():
    file_id = request.json['file_id']
    date_col = request.json['date_column']
    value_col = request.json['value_column']
    
    df = load_file(file_id)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    
    # Time series decomposition
    ts = df.set_index(date_col)[value_col]
    decomposition = seasonal_decompose(ts, model='additive', period=12)
    
    return {
        'trend': decomposition.trend.tolist(),
        'seasonal': decomposition.seasonal.tolist(),
        'residual': decomposition.resid.tolist()
    }
```

---

### 2.7 Comparative Analysis

#### Multi-Dataset Comparison
- **Compare two datasets**: Side-by-side metrics
- **Differences**: Which rows/values differ?
- **Quality comparison**: Which dataset is cleaner?

#### Benchmark Comparison
- **Industry benchmarks**: Compare to averages
- **Goal tracking**: Current vs target values
- **Performance ranking**: How you rank vs competitors

```python
@app.route('/api/analytics/compare', methods=['POST'])
def compare_datasets():
    file1_id = request.json['file1_id']
    file2_id = request.json['file2_id']
    
    df1 = load_file(file1_id)
    df2 = load_file(file2_id)
    
    comparison = {
        'df1_rows': len(df1),
        'df2_rows': len(df2),
        'df1_columns': list(df1.columns),
        'df2_columns': list(df2.columns),
        'common_columns': list(set(df1.columns) & set(df2.columns)),
        'df1_stats': df1.describe().to_dict(),
        'df2_stats': df2.describe().to_dict(),
    }
    
    return comparison
```

---

### 2.8 Custom Reporting

#### Report Builder
- **Select metrics**: Which KPIs to include
- **Select charts**: Which visualizations
- **Add narrative**: Write custom text/insights
- **Formatting options**: Colors, logos, branding
- **Export options**: PDF, PowerPoint, HTML

#### Scheduled Reports
- **Email reports**: Automatically send daily/weekly/monthly
- **Report templates**: Save and reuse
- **Distribution lists**: Define who receives each report

---

## Complete Feature List

### Part 1: Data Management (40+ Features)

#### File Management (5)
- [ ] Upload CSV/Excel/TSV files
- [ ] File browser & search
- [ ] Preview & statistics
- [ ] Download/export original
- [ ] Delete & version control

#### Data Cleaning (15)
- [ ] Handle missing values (drop, fill, interpolate)
- [ ] Remove duplicates (exact & fuzzy)
- [ ] Data type conversion & fixing
- [ ] Remove special characters & whitespace
- [ ] Detect & handle outliers
- [ ] Text normalization (case, trim, etc.)
- [ ] Data validation rules
- [ ] Pattern detection (email, phone, URL)
- [ ] Currency/number parsing
- [ ] Date parsing & formatting
- [ ] Encoding detection & conversion
- [ ] Column data quality scoring
- [ ] Null pattern detection
- [ ] Whitespace handling (leading/trailing/internal)
- [ ] HTML/markup tag removal

#### Row/Column Operations (8)
- [ ] Filter rows (simple & complex conditions)
- [ ] Select specific columns
- [ ] Rename columns (single & bulk)
- [ ] Reorder columns
- [ ] Delete rows/columns
- [ ] Select by pattern/regex
- [ ] Split data (percentage, condition, random)
- [ ] Row range selection

#### Data Transformation (12)
- [ ] Concatenate columns
- [ ] Split columns (by delimiter)
- [ ] Extract substrings (regex)
- [ ] Text replacement
- [ ] Math operations (add, subtract, multiply, divide)
- [ ] Binning/categorization
- [ ] Normalize/scale numeric data
- [ ] Create calculated columns
- [ ] Date calculations (age, duration)
- [ ] Mapping (value lookup)
- [ ] One-hot encoding
- [ ] Percentage/ratio calculations

#### Advanced Operations (8)
- [ ] Merge/join multiple files
- [ ] Concatenate/stack files
- [ ] Pivot tables with aggregation
- [ ] Group by & aggregation
- [ ] Sorting (single & multi-column)
- [ ] Ranking
- [ ] Cross-tabulation
- [ ] Top/bottom N selection

#### Export & Save (5)
- [ ] Export to CSV
- [ ] Export to Excel
- [ ] Export to JSON
- [ ] Save to database (PostgreSQL/MySQL)
- [ ] Schedule automated exports

#### Collaboration (2)
- [ ] Undo/Redo operations
- [ ] Operation history & audit log

---

### Part 2: Analytics & Visualization (35+ Features)

#### Data Profiling (8)
- [ ] Column-level statistics
- [ ] Data type detection
- [ ] Null/missing analysis
- [ ] Cardinality assessment
- [ ] Text pattern analysis
- [ ] Numeric distribution analysis
- [ ] Categorical value counts
- [ ] Auto-generated data quality report

#### Visualizations (10)
- [ ] Bar charts (vertical & horizontal)
- [ ] Pie charts
- [ ] Line charts (with trend lines)
- [ ] Scatter plots (with regression)
- [ ] Histograms & distributions
- [ ] Box plots (quartile analysis)
- [ ] Heatmaps (correlation, pivot)
- [ ] Area charts (stacked)
- [ ] Violin plots
- [ ] Word clouds (text data)

#### Statistical Analysis (8)
- [ ] Correlation analysis (Pearson, Spearman)
- [ ] Hypothesis testing (t-test, chi-square)
- [ ] Distribution analysis (normality tests)
- [ ] Outlier detection & analysis
- [ ] Variance analysis
- [ ] Regression analysis (linear, polynomial)
- [ ] Confidence intervals
- [ ] Effect size calculations

#### Descriptive Statistics (7)
- [ ] Mean, median, mode
- [ ] Standard deviation & variance
- [ ] Min, max, range
- [ ] Quartiles & percentiles
- [ ] Skewness & kurtosis
- [ ] Auto-generated insights & narratives
- [ ] Custom summary creation

#### Segmentation & Grouping (5)
- [ ] Customer/data segmentation
- [ ] Cohort analysis
- [ ] Segment comparison
- [ ] RFM analysis
- [ ] Behavioral clustering

#### Time-Series Analysis (5)
- [ ] Trend analysis
- [ ] Seasonality detection
- [ ] Forecasting (ARIMA, Prophet)
- [ ] Lag/lead analysis
- [ ] Moving averages & smoothing

#### Comparative Analysis (2)
- [ ] Multi-dataset comparison
- [ ] Benchmark analysis

#### Reporting (2)
- [ ] Custom report builder
- [ ] Scheduled email reports

---

## Technical Stack

### Frontend
- **Framework**: React 18.x
- **Styling**: Tailwind CSS 3.x + custom CSS
- **Charts**: Recharts / Plotly.js
- **State Management**: Redux Toolkit / Zustand
- **Data Table**: React Table (TanStack Table)
- **File Upload**: React Dropzone
- **Form Handling**: React Hook Form
- **UI Components**: Shadcn/ui or Material-UI
- **Build Tool**: Vite
- **Package Manager**: npm / yarn

### Backend
- **Framework**: FastAPI or Flask
- **Language**: Python 3.9+
- **ORM**: SQLAlchemy
- **API Documentation**: Swagger/OpenAPI
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Statistics**: SciPy, Statsmodels
- **CSV/Excel**: Openpyxl, XlsxWriter
- **Async**: Celery for long-running tasks
- **Caching**: Redis

### Database
- **Primary**: PostgreSQL 13+
- **In-memory Cache**: Redis
- **File Storage**: Local filesystem / AWS S3 / Azure Blob Storage

### Deployment
- **Docker**: Containerization
- **CI/CD**: GitHub Actions / GitLab CI
- **Server**: Nginx (reverse proxy)
- **App Server**: Gunicorn (Python)
- **Cloud**: AWS EC2 / DigitalOcean / Heroku

### Development Tools
- **Version Control**: Git
- **Code Quality**: Black, Flake8, Pylint
- **Testing**: Pytest (backend), Jest (frontend)
- **Documentation**: Sphinx / MkDocs
- **Logging**: Python logging + ELK Stack (optional)

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (or SQLite for development)
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/datavault.git
cd datavault/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
python -m flask db upgrade
# or for SQLAlchemy migrations
alembic upgrade head

# Run backend server
python app.py
# or with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Update API_URL to point to backend

# Run development server
npm run dev

# Build for production
npm run build
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# API Docs: http://localhost:5000/docs
```

---

## User Guide

### Part 1: Data Management Workflow

**Step 1: Upload File**
1. Click "Upload CSV" button
2. Select file or drag-and-drop
3. Preview data
4. Click "Load"

**Step 2: Clean Data**
1. Review "Data Quality" panel
2. Handle missing values:
   - Click "Handle Missing" → select operation
   - Choose column(s) → apply
3. Remove duplicates:
   - Click "Remove Duplicates"
   - Select columns to check → apply
4. Fix data types:
   - Click "Data Types"
   - For each column, verify/change type

**Step 3: Transform Data**
1. Click "Transform" section
2. Select operation (concatenate, split, extract, etc.)
3. Configure parameters
4. Preview result
5. Apply

**Step 4: Filter/Select**
1. Click "Filter" to apply row conditions
2. Click "Select Columns" to choose columns
3. Use drag-and-drop to reorder
4. "Split Data" to create subsets

**Step 5: Export**
1. Click "Export"
2. Choose format (CSV, Excel, JSON, Database)
3. Download or save to platform

---

### Part 2: Analytics Workflow

**Step 1: Profile Data**
1. Upload file or select existing
2. Click "Analytics" tab
3. Review auto-generated profile

**Step 2: Visualize**
1. Click "Charts"
2. Select chart type
3. Choose X/Y columns
4. Customize (colors, labels, etc.)
5. View interactive chart

**Step 3: Analyze**
1. Click "Analysis"
2. Select analysis type (correlation, outliers, trends)
3. Configure parameters
4. View results & insights

**Step 4: Create Report**
1. Click "Reports"
2. Select metrics/charts
3. Add narrative text
4. Customize formatting
5. Export/email

---

## API Endpoints

### File Management
```
POST   /api/files/upload              - Upload CSV file
GET    /api/files                     - List all files
GET    /api/files/<id>                - Get file details
GET    /api/files/<id>/preview        - Preview file (first N rows)
DELETE /api/files/<id>                - Delete file
GET    /api/files/<id>/download       - Download file
```

### Data Operations
```
POST   /api/operations/filter         - Filter rows
POST   /api/operations/select_cols    - Select columns
POST   /api/operations/split          - Split data
POST   /api/operations/handle_missing - Handle nulls
POST   /api/operations/remove_dupes   - Remove duplicates
POST   /api/operations/convert_type   - Convert data types
POST   /api/operations/clean_text     - Text cleaning
POST   /api/operations/transform      - Data transformation
POST   /api/operations/merge          - Merge files
POST   /api/operations/pivot          - Create pivot table
POST   /api/operations/groupby        - Group & aggregate
POST   /api/operations/sort           - Sort data
```

### Export
```
POST   /api/export/csv                - Export to CSV
POST   /api/export/excel              - Export to Excel
POST   /api/export/database           - Export to database
POST   /api/export/email              - Email CSV file
```

### Analytics
```
GET    /api/analytics/profile/<id>    - Data profile/quality report
GET    /api/analytics/summary/<id>    - Summary statistics
GET    /api/analytics/correlation    - Correlation analysis
GET    /api/analytics/outliers       - Outlier detection
GET    /api/analytics/trends         - Trend analysis
POST   /api/charts/create             - Create visualization
GET    /api/analytics/segments        - Segment analysis
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Files Table
```sql
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT,
    rows INT,
    columns INT,
    encoding VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### Operations History Table
```sql
CREATE TABLE operations_history (
    id SERIAL PRIMARY KEY,
    file_id INT NOT NULL,
    operation_type VARCHAR(50),
    operation_config JSONB,
    result_file_id INT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (result_file_id) REFERENCES files(id)
);
```

---

## Key Features Summary

### Why DataVault?

✅ **No Coding Required** - Complex data operations via UI
✅ **Time Saving** - 80% faster than manual Excel work
✅ **Professional Quality** - Enterprise-grade data handling
✅ **Audit Trail** - Track all changes with undo/redo
✅ **Scalable** - Handle files from KB to GB
✅ **Secure** - Role-based access, encrypted storage
✅ **Collaborative** - Share projects and reports
✅ **Export Flexibility** - Multiple format support
✅ **Data Insights** - Automated analytics & visualizations
✅ **Integration Ready** - API for external systems

---

## Roadmap

### Phase 1 (MVP - 8 weeks)
- File upload & management
- Basic cleaning operations (nulls, duplicates, types)
- Row/column filtering & selection
- Export to CSV/Excel
- Basic charts (bar, pie, line)
- Data profiling

### Phase 2 (2 months)
- Advanced cleaning (outliers, text, dates)
- Data transformation (concatenate, split, extract)
- Merge/join operations
- Statistical analysis
- More chart types
- Scheduled exports

### Phase 3 (3 months)
- AI-powered data quality suggestions
- Automated insights & narratives
- Custom reporting
- Database connectors
- API access
- Mobile app

### Phase 4+ (Future)
- Machine learning pipeline builder
- Real-time data streaming
- Advanced forecasting
- Collaborative workspace
- Enterprise features (SSO, audit logs, etc.)

---

## Support & Contact

- **Documentation**: [docs.datavault.com](https://docs.datavault.com)
- **GitHub Issues**: Report bugs and request features
- **Email**: support@datavault.com
- **Community Forum**: [community.datavault.com](https://community.datavault.com)

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

- Built with ❤️ for data professionals
- Inspired by modern data tools and best practices
- Community-driven development

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Status**: In Development
