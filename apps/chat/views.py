from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import uuid
import re
from .models import ChatSession, ChatMessage, ChatBotResponse


@csrf_exempt
def chat_api(request):
    """Chat API endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'start_session':
                return start_chat_session(request, data)
            elif action == 'send_message':
                return send_message(request, data)
            elif action == 'get_messages':
                return get_messages(request, data)
            elif action == 'end_session':
                return end_chat_session(request, data)
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def start_chat_session(request, data):
    """Start a new chat session"""
    session_id = str(uuid.uuid4())
    visitor_name = data.get('visitor_name', '')
    visitor_email = data.get('visitor_email', '')
    
    session = ChatSession.objects.create(
        session_id=session_id,
        user=request.user if request.user.is_authenticated else None,
        visitor_name=visitor_name,
        visitor_email=visitor_email
    )
    
    # Send welcome message
    welcome_message = get_bot_response("greeting")
    ChatMessage.objects.create(
        session=session,
        message_type='bot',
        content=welcome_message
    )
    
    return JsonResponse({
        'success': True,
        'session_id': session_id,
        'welcome_message': welcome_message
    })


def send_message(request, data):
    """Send a message in chat"""
    session_id = data.get('session_id')
    message_content = data.get('message', '').strip()
    
    try:
        session = ChatSession.objects.get(session_id=session_id, is_active=True)
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid session'})
    
    if not message_content:
        return JsonResponse({'success': False, 'error': 'Message cannot be empty'})
    
    # Save user message
    user_message = ChatMessage.objects.create(
        session=session,
        message_type='user',
        content=message_content
    )
    
    # Generate bot response
    bot_response = get_bot_response(message_content)
    bot_message = ChatMessage.objects.create(
        session=session,
        message_type='bot',
        content=bot_response
    )
    
    return JsonResponse({
        'success': True,
        'user_message': {
            'id': user_message.id,
            'content': user_message.content,
            'timestamp': user_message.timestamp.isoformat()
        },
        'bot_response': {
            'id': bot_message.id,
            'content': bot_message.content,
            'timestamp': bot_message.timestamp.isoformat()
        }
    })


def get_messages(request, data):
    """Get chat messages for a session"""
    session_id = data.get('session_id')
    
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.all()
        
        message_list = []
        for msg in messages:
            message_list.append({
                'id': msg.id,
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'messages': message_list
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid session'})


def end_chat_session(request, data):
    """End a chat session"""
    session_id = data.get('session_id')
    
    try:
        session = ChatSession.objects.get(session_id=session_id, is_active=True)
        session.is_active = False
        session.ended_at = timezone.now()
        session.save()
        
        return JsonResponse({'success': True, 'message': 'Chat session ended'})
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid session'})


def get_bot_response(user_input):
    """Generate bot response based on user input with enhanced conversation"""
    user_input_lower = user_input.lower().strip()

    # Enhanced greeting responses
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings', 'hola', 'howdy', 'sup', 'yo']
    if any(greeting in user_input_lower for greeting in greetings):
        greeting_responses = [
            "Hello! 👋 Welcome to my data science portfolio! I'm here to help you explore my projects, skills, and services. What would you like to know?",
            "Hi there! 😊 Great to meet you! I'm Muna, an AI assistant helping visitors learn about my data science work. How can I assist you today?",
            "Hey! 🚀 Thanks for stopping by! I'm excited to help you discover my data science projects and capabilities. What interests you most?",
            "Good day! ✨ I'm here to guide you through my portfolio and answer any questions about my data science expertise. What can I help you with?",
            "Greetings! 🌟 I'm your personal guide to this data science portfolio. Feel free to ask me anything about projects, skills, or services!",
            "Hello and welcome! 🎯 I'm here to make your visit informative and engaging. What aspect of data science interests you most?"
        ]
        import random
        return random.choice(greeting_responses)

    # Thank you responses
    thanks = ['thank', 'thanks', 'appreciate', 'grateful']
    if any(thank in user_input_lower for thank in thanks):
        return "You're very welcome! 😊 I'm always happy to help. Is there anything else you'd like to know about my data science work or services?"

    # Goodbye responses
    goodbyes = ['bye', 'goodbye', 'see you', 'farewell', 'take care', 'later']
    if any(goodbye in user_input_lower for goodbye in goodbyes):
        return "Thank you for visiting! 👋 Feel free to explore my portfolio, and don't hesitate to reach out through the contact form if you have any questions. Have a great day!"

    # HOW questions - comprehensive handling
    if user_input_lower.startswith('how'):
        how_responses = {
            'how are you': "I'm doing fantastic! 😊 I'm here and ready to help you explore data science projects and services. How are you doing today?",
            'how do you': "I'm Muna, an AI assistant designed to help visitors navigate this data science portfolio. I can answer questions about projects, skills, technologies, and services!",
            'how can': "I can help you in many ways! 🚀 I can explain projects, discuss technologies, provide code examples, suggest project ideas, and guide you through services. What specifically interests you?",
            'how much': "💰 Project pricing varies by complexity:\n• Simple analysis: $200-500\n• ML models: $500-2000\n• Full solutions: $1000-5000+\n\nFor accurate quotes, please use the 'Request Project' feature!",
            'how long': "⏰ Project timelines depend on scope:\n• Data analysis: 1-2 weeks\n• ML models: 2-4 weeks\n• Complex systems: 1-3 months\n\nI always provide detailed timelines during consultation!",
            'how to': "🎯 I'd love to help you learn! What specific topic would you like guidance on? I can explain:\n• Data science concepts\n• Programming techniques\n• Project methodologies\n• Technology choices",
        }

        for key, response in how_responses.items():
            if key in user_input_lower:
                return response

        return "🤔 That's a great 'how' question! I'm here to help with data science topics. Could you be more specific about what you'd like to know how to do?"

    # WHAT questions - comprehensive handling
    if user_input_lower.startswith('what'):
        what_responses = {
            'what is': "🧠 I can explain many data science concepts! What specific topic would you like me to explain? I know about:\n• Machine Learning\n• Data Analysis\n• Python/R programming\n• Statistics\n• Databases\n• Visualization",
            'what are': "📊 I can discuss various data science topics! What specifically are you curious about? I can explain technologies, methodologies, career paths, or project types.",
            'what can': "🚀 I can help with many things!\n• Explain data science concepts\n• Suggest project ideas\n• Provide code examples\n• Discuss technologies\n• Generate project titles\n• Create project descriptions\n\nWhat would you like me to help with?",
            'what do': "💼 In data science, we:\n• Analyze data to find insights\n• Build predictive models\n• Create visualizations\n• Solve business problems\n• Automate processes\n• Make data-driven decisions\n\nWhat specific aspect interests you?",
            'what technologies': "🛠️ I work with cutting-edge technologies:\n• Python (Pandas, NumPy, Scikit-learn)\n• Machine Learning (TensorFlow, PyTorch)\n• Databases (SQL, MongoDB)\n• Visualization (Matplotlib, Plotly, Tableau)\n• Cloud (AWS, Azure, GCP)\n• Big Data (Spark, Hadoop)",
            'what projects': "📈 I've worked on diverse projects:\n• Predictive Analytics\n• Customer Segmentation\n• Fraud Detection\n• Recommendation Systems\n• Time Series Forecasting\n• NLP Applications\n\nWhich type interests you most?",
            'what services': "🎯 I offer comprehensive data science services:\n• Custom Analytics Solutions\n• Machine Learning Development\n• Data Visualization Dashboards\n• Business Intelligence\n• Consulting & Training\n• Data Strategy Planning",
        }

        for key, response in what_responses.items():
            if key in user_input_lower:
                return response

        return "🤔 That's an interesting 'what' question! I'm here to explain data science concepts, technologies, and services. What specifically would you like to know about?"

    # WHICH questions - comprehensive handling
    if user_input_lower.startswith('which'):
        which_responses = {
            'which technology': "🛠️ The best technology depends on your needs:\n• Python: Versatile, great for beginners\n• R: Excellent for statistics\n• SQL: Essential for databases\n• Tableau: Best for visualization\n• TensorFlow: Deep learning\n\nWhat's your specific use case?",
            'which language': "💻 For data science, I recommend:\n• Python (most popular, versatile)\n• R (statistical analysis)\n• SQL (database queries)\n• JavaScript (web visualization)\n• Scala (big data with Spark)\n\nWhat type of projects interest you?",
            'which tool': "🔧 Popular data science tools:\n• Jupyter Notebooks (development)\n• Pandas (data manipulation)\n• Scikit-learn (machine learning)\n• Matplotlib/Seaborn (visualization)\n• Git (version control)\n\nWhat task are you trying to accomplish?",
            'which project': "📊 I can suggest projects based on your interests:\n• Beginner: Data visualization, basic analysis\n• Intermediate: Predictive modeling, classification\n• Advanced: Deep learning, NLP, computer vision\n\nWhat's your experience level?",
        }

        for key, response in which_responses.items():
            if key in user_input_lower:
                return response

        return "🎯 Great 'which' question! I can help you choose between technologies, tools, or approaches. What options are you considering?"

    # WHO questions - comprehensive handling
    if user_input_lower.startswith('who'):
        who_responses = {
            'who are you': "👋 I'm Muna, an AI assistant for Adrian! I'm here to help you learn about projects, skills, and services. Think of me as your personal guide to data science expertise!",
            'who is': "🤔 If you're asking about me, I'm Muna, an AI assistant specializing in data science topics. If you're asking about someone else, could you be more specific?",
            'who can': "🙋‍♂️ I can help you with data science questions! I can explain concepts, suggest projects, provide code examples, and guide you through services. What do you need help with?",
            'who should': "💡 For data science career advice:\n• Students: Start with Python and statistics\n• Professionals: Focus on domain expertise + data skills\n• Businesses: Consider hiring data scientists or consultants\n\nWhat's your situation?",
        }

        for key, response in who_responses.items():
            if key in user_input_lower:
                return response

        return "👤 I'm here to help with 'who' questions! Are you asking about me, career advice, or someone specific in data science?"

    # "Are you able to" and capability questions
    if any(phrase in user_input_lower for phrase in ['can you create', 'can you build', 'can you develop', 'can you make']):
        capability_responses = [
            "🚀 Absolutely! I can help create various data science projects:\n\n• **Predictive Analytics**: Customer behavior, sales forecasting\n• **Machine Learning Models**: Classification, regression, clustering\n• **Data Dashboards**: Interactive visualizations and reports\n• **Automation Tools**: Data pipelines, ETL processes\n• **NLP Applications**: Sentiment analysis, chatbots\n• **Computer Vision**: Image recognition, object detection\n\nWhat type of project do you have in mind?",

            "✅ Yes! I specialize in building custom data science solutions:\n\n• **Business Intelligence**: KPI dashboards, performance metrics\n• **Recommendation Systems**: Product/content recommendations\n• **Fraud Detection**: Anomaly detection systems\n• **Time Series Analysis**: Trend analysis, forecasting\n• **Web Scraping**: Data collection and processing\n• **API Development**: Data service endpoints\n\nTell me about your specific requirements!",

            "💡 Definitely! I can develop comprehensive solutions:\n\n• **Data Analysis**: Statistical analysis, hypothesis testing\n• **Visualization Tools**: Interactive charts, maps, reports\n• **Machine Learning**: Supervised/unsupervised learning\n• **Deep Learning**: Neural networks, AI models\n• **Database Solutions**: Data warehousing, optimization\n• **Cloud Deployment**: Scalable, production-ready systems\n\nWhat challenge are you trying to solve?"
        ]

        import random
        return random.choice(capability_responses)

    # Project title and description generation
    if any(phrase in user_input_lower for phrase in ['generate project title', 'project title', 'suggest title', 'project name', 'title ideas']):
        project_titles = [
            "🎯 **Data Science Project Title Ideas:**\n\n• **Smart Customer Analytics Dashboard**\n• **Predictive Sales Forecasting System**\n• **AI-Powered Recommendation Engine**\n• **Real-time Fraud Detection Platform**\n• **Social Media Sentiment Analyzer**\n• **Automated Report Generation Tool**\n• **Customer Churn Prediction Model**\n• **Dynamic Pricing Optimization System**\n\nWould you like descriptions for any of these?",

            "💡 **Creative Project Titles:**\n\n• **Intelligent Business Intelligence Hub**\n• **Machine Learning Market Predictor**\n• **Data-Driven Decision Support System**\n• **Automated Anomaly Detection Engine**\n• **Interactive Data Storytelling Platform**\n• **Smart Inventory Management System**\n• **Personalized Content Recommendation AI**\n• **Advanced Analytics Command Center**\n\nWhich domain interests you most?",

            "🚀 **Innovative Project Names:**\n\n• **NextGen Data Analytics Suite**\n• **AI-Enhanced Performance Monitor**\n• **Predictive Maintenance Optimizer**\n• **Smart Risk Assessment Platform**\n• **Automated Insights Generator**\n• **Dynamic Customer Segmentation Tool**\n• **Real-time Market Intelligence System**\n• **Intelligent Process Automation Hub**\n\nNeed detailed descriptions for any?"
        ]

        import random
        return random.choice(project_titles)

    # Project description generation
    if any(phrase in user_input_lower for phrase in ['project description', 'describe project', 'project details', 'project summary']):
        descriptions = [
            "📋 **Sample Project Description:**\n\n**Customer Analytics Dashboard**\n\n*Objective:* Build an interactive dashboard to analyze customer behavior and improve business decisions.\n\n*Features:*\n• Real-time customer metrics\n• Segmentation analysis\n• Purchase pattern visualization\n• Predictive lifetime value\n• Churn risk indicators\n\n*Technologies:* Python, Plotly, SQL, Machine Learning\n*Timeline:* 3-4 weeks\n*Deliverables:* Interactive dashboard, documentation, training\n\nWant a custom description for your project?",

            "📊 **Example Project Outline:**\n\n**Sales Forecasting System**\n\n*Purpose:* Develop ML models to predict future sales and optimize inventory.\n\n*Components:*\n• Historical data analysis\n• Seasonal trend detection\n• Multiple forecasting models\n• Accuracy comparison\n• Automated reporting\n\n*Tech Stack:* Python, Scikit-learn, Pandas, Tableau\n*Duration:* 2-3 weeks\n*Outcomes:* Improved planning, reduced costs, better decisions\n\nNeed a description for a specific project type?"
        ]

        import random
        return random.choice(descriptions)

    # Questions about the portfolio owner
    if any(phrase in user_input_lower for phrase in ['about you', 'tell me about', 'your background', 'your experience', 'who owns', 'portfolio owner']):
        about_responses = [
            "👨‍💻 **About the Portfolio Owner:**\n\n🎓 Currently pursuing Bachelor of Commerce Honours in Data Science & Informatics\n\n💼 **Expertise Areas:**\n• Python Programming & Data Analysis\n• Machine Learning & AI Development\n• Business Intelligence & Visualization\n• Statistical Analysis & Modeling\n• Database Management & SQL\n\n🌟 **Passion:** Transforming data into actionable insights that drive business success!\n\n📍 **Location:** Zimbabwe\n🎯 **Mission:** Making data science accessible and impactful for businesses of all sizes",

            "🚀 **Professional Profile:**\n\n📚 **Education:** Data Science & Informatics Honours Student\n\n🛠️ **Technical Skills:**\n• Advanced Python (Pandas, NumPy, Scikit-learn)\n• Machine Learning & Deep Learning\n• Data Visualization (Matplotlib, Plotly, Tableau)\n• SQL & Database Management\n• Cloud Platforms (AWS, Azure)\n• Statistical Analysis & Research\n\n💡 **Specializations:**\n• Predictive Analytics\n• Business Intelligence\n• Custom Data Solutions\n• Automation & Process Optimization\n\n🎯 **Goal:** Helping businesses unlock the power of their data!"
        ]

        import random
        return random.choice(about_responses)

    # Technology-specific detailed responses
    if 'python' in user_input_lower and any(word in user_input_lower for word in ['tell', 'about', 'explain', 'what']):
        return "🐍 **Python for Data Science:**\n\n**Why Python?**\n• Easy to learn and read\n• Massive ecosystem of libraries\n• Great community support\n• Versatile for web, data, AI\n\n**Key Libraries:**\n• **Pandas**: Data manipulation\n• **NumPy**: Numerical computing\n• **Matplotlib/Seaborn**: Visualization\n• **Scikit-learn**: Machine learning\n• **TensorFlow/PyTorch**: Deep learning\n\n**Use Cases:**\n• Data cleaning and analysis\n• Machine learning models\n• Web scraping\n• Automation scripts\n• API development\n\nWant to see some Python code examples?"

    if 'machine learning' in user_input_lower and any(word in user_input_lower for word in ['explain', 'what', 'tell', 'about']):
        return "🤖 **Machine Learning Explained:**\n\n**What is ML?**\nAlgorithms that learn patterns from data to make predictions or decisions without explicit programming.\n\n**Types:**\n• **Supervised**: Learning with labeled data (classification, regression)\n• **Unsupervised**: Finding patterns in unlabeled data (clustering)\n• **Reinforcement**: Learning through trial and error\n\n**Popular Algorithms:**\n• Linear/Logistic Regression\n• Random Forest\n• Support Vector Machines\n• Neural Networks\n• K-Means Clustering\n\n**Applications:**\n• Recommendation systems\n• Fraud detection\n• Image recognition\n• Natural language processing\n• Predictive analytics\n\nWhich ML topic interests you most?"

    if 'data science' in user_input_lower and any(word in user_input_lower for word in ['explain', 'what', 'about', 'field']):
        return "📊 **Data Science Overview:**\n\n**Definition:**\nInterdisciplinary field using scientific methods, algorithms, and systems to extract insights from structured and unstructured data.\n\n**Key Components:**\n• **Statistics**: Understanding data distributions\n• **Programming**: Python, R, SQL\n• **Machine Learning**: Predictive modeling\n• **Domain Expertise**: Business understanding\n• **Communication**: Storytelling with data\n\n**Process (CRISP-DM):**\n1. Business Understanding\n2. Data Understanding\n3. Data Preparation\n4. Modeling\n5. Evaluation\n6. Deployment\n\n**Career Paths:**\n• Data Analyst\n• Data Scientist\n• ML Engineer\n• Data Engineer\n• Business Intelligence Analyst\n\nWhat aspect would you like to explore?"

    # Code snippet generation
    if any(phrase in user_input_lower for phrase in ['code example', 'show code', 'code snippet', 'python code', 'sample code']):
        code_examples = [
            "💻 **Python Data Analysis Example:**\n\n```python\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n# Load and explore data\ndf = pd.read_csv('data.csv')\nprint(df.head())\nprint(df.info())\n\n# Basic statistics\nprint(df.describe())\n\n# Simple visualization\ndf['column'].hist()\nplt.title('Distribution')\nplt.show()\n\n# Group analysis\nresult = df.groupby('category')['value'].mean()\nprint(result)\n```\n\nWant to see more specific examples?",

            "🤖 **Machine Learning Code Example:**\n\n```python\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score\n\n# Prepare data\nX = df.drop('target', axis=1)\ny = df['target']\n\n# Split data\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42\n)\n\n# Train model\nmodel = RandomForestClassifier(n_estimators=100)\nmodel.fit(X_train, y_train)\n\n# Make predictions\npredictions = model.predict(X_test)\naccuracy = accuracy_score(y_test, predictions)\nprint(f'Accuracy: {accuracy:.2f}')\n```\n\nNeed help with a specific algorithm?",

            "📊 **Data Visualization Example:**\n\n```python\nimport plotly.express as px\nimport seaborn as sns\n\n# Interactive scatter plot\nfig = px.scatter(df, x='feature1', y='feature2', \n                color='category', size='value',\n                title='Interactive Scatter Plot')\nfig.show()\n\n# Correlation heatmap\nplt.figure(figsize=(10, 8))\nsns.heatmap(df.corr(), annot=True, cmap='coolwarm')\nplt.title('Correlation Matrix')\nplt.show()\n\n# Time series plot\ndf['date'] = pd.to_datetime(df['date'])\ndf.set_index('date')['value'].plot()\nplt.title('Time Series Analysis')\nplt.show()\n```\n\nWhat type of visualization do you need?"
        ]

        import random
        return random.choice(code_examples)

    # Informatics responses
    if 'informatics' in user_input_lower:
        return "🖥️ **Informatics Explained:**\n\n**Definition:**\nThe science of processing data for storage and retrieval; information science.\n\n**Key Areas:**\n• **Health Informatics**: Medical data systems\n• **Business Informatics**: Enterprise information systems\n• **Social Informatics**: Technology's impact on society\n• **Bio-informatics**: Computational biology\n• **Geo-informatics**: Geographic information systems\n\n**Skills Involved:**\n• Database design and management\n• System analysis and design\n• Information architecture\n• Data modeling\n• User interface design\n• Network systems\n\n**Career Opportunities:**\n• Systems Analyst\n• Database Administrator\n• Information Architect\n• IT Consultant\n• Business Analyst\n\n**Intersection with Data Science:**\nInformatics provides the foundation for data storage, retrieval, and system design that data science builds upon!\n\nInterested in a specific informatics area?"

    # Data science project ideas
    if any(phrase in user_input_lower for phrase in ['data science projects', 'project ideas', 'ds projects', 'analytics projects']):
        project_ideas = [
            "🚀 **Beginner Data Science Projects:**\n\n1. **Sales Analysis Dashboard**\n   • Analyze sales trends and patterns\n   • Create interactive visualizations\n   • Identify top products and regions\n\n2. **Customer Segmentation**\n   • Group customers by behavior\n   • RFM analysis (Recency, Frequency, Monetary)\n   • Targeted marketing strategies\n\n3. **Stock Price Prediction**\n   • Time series analysis\n   • Technical indicators\n   • Simple forecasting models\n\n4. **Social Media Sentiment Analysis**\n   • Text preprocessing\n   • Sentiment classification\n   • Trend analysis\n\n5. **House Price Prediction**\n   • Feature engineering\n   • Regression modeling\n   • Model evaluation\n\nWhich project type interests you most?",

            "💡 **Intermediate Data Science Projects:**\n\n1. **Recommendation System**\n   • Collaborative filtering\n   • Content-based recommendations\n   • Hybrid approaches\n\n2. **Fraud Detection System**\n   • Anomaly detection\n   • Classification algorithms\n   • Real-time monitoring\n\n3. **Churn Prediction Model**\n   • Customer lifetime value\n   • Survival analysis\n   • Retention strategies\n\n4. **Image Classification**\n   • Convolutional Neural Networks\n   • Transfer learning\n   • Computer vision\n\n5. **Chatbot Development**\n   • Natural Language Processing\n   • Intent recognition\n   • Response generation\n\nNeed detailed guidance for any project?",

            "🎯 **Advanced Data Science Projects:**\n\n1. **Real-time Analytics Platform**\n   • Stream processing\n   • Apache Kafka/Spark\n   • Live dashboards\n\n2. **Deep Learning for NLP**\n   • Transformer models\n   • BERT/GPT implementations\n   • Language understanding\n\n3. **Computer Vision Pipeline**\n   • Object detection\n   • Image segmentation\n   • Video analysis\n\n4. **MLOps Implementation**\n   • Model deployment\n   • Continuous integration\n   • Monitoring and maintenance\n\n5. **Multi-modal AI System**\n   • Text + Image analysis\n   • Cross-modal learning\n   • Unified embeddings\n\nReady for a challenge? Which interests you?"
        ]

        import random
        return random.choice(project_ideas)

    # Multiple question handling
    if any(phrase in user_input_lower for phrase in ['and', 'also', 'plus', 'additionally', 'furthermore']):
        return "🤔 I see you have multiple questions! I'm happy to help with all of them. Could you break them down one by one? I can provide detailed answers for each topic:\n\n• Data science concepts\n• Technology explanations\n• Project guidance\n• Code examples\n• Career advice\n• Service information\n\nWhat would you like to explore first?"

    # Learning and education responses
    if any(phrase in user_input_lower for phrase in ['learn', 'study', 'education', 'course', 'tutorial', 'guide']):
        learning_responses = [
            "📚 **Learning Data Science Path:**\n\n**Step 1: Foundations**\n• Mathematics (Statistics, Linear Algebra)\n• Programming (Python/R)\n• SQL and Databases\n\n**Step 2: Core Skills**\n• Data Manipulation (Pandas, NumPy)\n• Visualization (Matplotlib, Plotly)\n• Machine Learning (Scikit-learn)\n\n**Step 3: Specialization**\n• Deep Learning (TensorFlow/PyTorch)\n• Big Data (Spark, Hadoop)\n• Cloud Platforms (AWS, Azure)\n\n**Step 4: Practice**\n• Kaggle competitions\n• Personal projects\n• Open source contributions\n\n**Resources:**\n• Online courses (Coursera, edX)\n• Books and documentation\n• YouTube tutorials\n• Practice datasets\n\nWhat's your current level?",

            "🎓 **Data Science Education Guide:**\n\n**Free Resources:**\n• Python.org tutorials\n• Kaggle Learn courses\n• YouTube (3Blue1Brown, StatQuest)\n• GitHub repositories\n• Medium articles\n\n**Paid Courses:**\n• Coursera Data Science Specialization\n• edX MicroMasters programs\n• Udacity Nanodegrees\n• DataCamp interactive courses\n\n**Books to Read:**\n• 'Python for Data Analysis' - Wes McKinney\n• 'Hands-On ML' - Aurélien Géron\n• 'The Elements of Statistical Learning'\n• 'Data Science from Scratch'\n\n**Practice Platforms:**\n• Kaggle competitions\n• HackerRank\n• LeetCode\n• Google Colab\n\nWhich learning style suits you best?"
        ]

        import random
        return random.choice(learning_responses)

    # Business and industry responses
    if any(phrase in user_input_lower for phrase in ['business', 'industry', 'company', 'enterprise', 'commercial']):
        return "💼 **Data Science in Business:**\n\n**Key Applications:**\n• **Customer Analytics**: Behavior analysis, segmentation\n• **Predictive Maintenance**: Equipment failure prediction\n• **Supply Chain Optimization**: Demand forecasting\n• **Risk Management**: Credit scoring, fraud detection\n• **Marketing Analytics**: Campaign optimization, ROI\n• **Operations Research**: Process optimization\n\n**Business Value:**\n• Increased revenue (10-20% typical)\n• Cost reduction (15-25%)\n• Better decision making\n• Competitive advantage\n• Customer satisfaction improvement\n\n**Implementation Strategy:**\n1. Identify business problems\n2. Assess data availability\n3. Start with pilot projects\n4. Scale successful solutions\n5. Build data culture\n\n**ROI Examples:**\n• Netflix saves $1B annually with recommendations\n• Amazon's algorithms drive 35% of sales\n• Walmart reduced inventory costs by 10%\n\nWhat business challenge interests you?"

    # Career and job-related responses
    if any(phrase in user_input_lower for phrase in ['career', 'job', 'salary', 'employment', 'hiring', 'work']):
        career_responses = [
            "💼 **Data Science Career Guide:**\n\n**Entry-Level Positions:**\n• Data Analyst ($45K-70K)\n• Junior Data Scientist ($60K-85K)\n• Business Intelligence Analyst ($50K-75K)\n\n**Mid-Level Positions:**\n• Data Scientist ($80K-120K)\n• ML Engineer ($90K-130K)\n• Data Engineer ($85K-125K)\n\n**Senior-Level Positions:**\n• Senior Data Scientist ($120K-180K)\n• Principal Data Scientist ($150K-250K)\n• Chief Data Officer ($200K-400K)\n\n**Skills in Demand:**\n• Python/R programming\n• Machine learning\n• Cloud platforms (AWS, Azure)\n• Deep learning\n• MLOps\n\n**Career Tips:**\n• Build a strong portfolio\n• Contribute to open source\n• Network with professionals\n• Stay updated with trends\n• Practice communication skills\n\nWhat career aspect interests you most?",

            "🚀 **Breaking into Data Science:**\n\n**Essential Skills:**\n• Programming (Python/R)\n• Statistics and mathematics\n• Data visualization\n• Machine learning\n• Domain expertise\n• Communication skills\n\n**Portfolio Projects:**\n• End-to-end ML projects\n• Data analysis case studies\n• Visualization dashboards\n• Web applications\n• Kaggle competitions\n\n**Job Search Strategy:**\n• Tailor resume for each role\n• Showcase projects on GitHub\n• Network on LinkedIn\n• Attend meetups and conferences\n• Practice technical interviews\n\n**Interview Preparation:**\n• Technical coding challenges\n• Statistics and ML concepts\n• Case study presentations\n• Behavioral questions\n• Portfolio walkthrough\n\nNeed help with any specific area?"
        ]

        import random
        return random.choice(career_responses)

    # Advanced technology discussions
    if any(phrase in user_input_lower for phrase in ['ai', 'artificial intelligence', 'deep learning', 'neural network']):
        ai_responses = [
            "🧠 **Artificial Intelligence & Deep Learning:**\n\n**AI Hierarchy:**\n• **Artificial Intelligence**: Broad field of machine intelligence\n• **Machine Learning**: Subset using algorithms to learn\n• **Deep Learning**: Subset using neural networks\n\n**Neural Network Types:**\n• **Feedforward**: Basic pattern recognition\n• **CNN**: Image processing, computer vision\n• **RNN/LSTM**: Sequential data, time series\n• **Transformer**: Language models, attention\n• **GAN**: Generative models, synthetic data\n\n**Applications:**\n• Image recognition and classification\n• Natural language processing\n• Speech recognition and synthesis\n• Autonomous vehicles\n• Game playing (AlphaGo, Chess)\n• Drug discovery\n\n**Frameworks:**\n• TensorFlow (Google)\n• PyTorch (Facebook)\n• Keras (High-level API)\n• JAX (Research)\n\nWhich AI application interests you most?",

            "🤖 **Deep Learning Explained:**\n\n**What makes it 'Deep'?**\nMultiple hidden layers that learn hierarchical representations of data.\n\n**Key Concepts:**\n• **Neurons**: Basic processing units\n• **Layers**: Groups of neurons\n• **Weights**: Learnable parameters\n• **Activation Functions**: Non-linear transformations\n• **Backpropagation**: Learning algorithm\n• **Gradient Descent**: Optimization method\n\n**Popular Architectures:**\n• **ResNet**: Skip connections for very deep networks\n• **BERT**: Bidirectional language understanding\n• **GPT**: Generative pre-trained transformers\n• **YOLO**: Real-time object detection\n• **U-Net**: Image segmentation\n\n**Training Requirements:**\n• Large datasets\n• Powerful GPUs\n• Significant compute time\n• Careful hyperparameter tuning\n\nWant to dive deeper into any architecture?"
        ]

        import random
        return random.choice(ai_responses)

    # Database and SQL responses
    if any(phrase in user_input_lower for phrase in ['sql', 'database', 'query', 'data storage']):
        return "🗄️ **SQL & Databases for Data Science:**\n\n**Why SQL is Essential:**\n• Most data is stored in databases\n• Efficient data retrieval\n• Data cleaning and preprocessing\n• Aggregations and joins\n• Integration with Python/R\n\n**Key SQL Concepts:**\n• **SELECT**: Retrieve data\n• **WHERE**: Filter conditions\n• **GROUP BY**: Aggregate data\n• **JOIN**: Combine tables\n• **WINDOW FUNCTIONS**: Advanced analytics\n\n**Database Types:**\n• **Relational**: PostgreSQL, MySQL, SQL Server\n• **NoSQL**: MongoDB, Cassandra\n• **Cloud**: BigQuery, Redshift, Snowflake\n• **In-Memory**: Redis, SAP HANA\n\n**Data Science SQL:**\n```sql\nSELECT \n    customer_id,\n    COUNT(*) as order_count,\n    AVG(order_value) as avg_order,\n    MAX(order_date) as last_order\nFROM orders \nWHERE order_date >= '2023-01-01'\nGROUP BY customer_id\nHAVING COUNT(*) > 5\nORDER BY avg_order DESC;\n```\n\nNeed help with specific SQL queries?"

    # Dynamic keyword-based response generation
    keywords_responses = {
        'visualization': "📊 **Data Visualization:**\n\nTurning data into visual stories! I can create:\n• Interactive dashboards\n• Statistical charts\n• Geographic maps\n• Real-time monitoring\n• Custom visualizations\n\nTools: Plotly, Tableau, D3.js, Matplotlib\nWant to see examples?",

        'statistics': "📈 **Statistics in Data Science:**\n\nFoundational concepts:\n• Descriptive statistics\n• Hypothesis testing\n• Probability distributions\n• Regression analysis\n• Bayesian methods\n• A/B testing\n\nEssential for understanding data patterns and making valid inferences!",

        'cloud': "☁️ **Cloud Computing for Data Science:**\n\nPlatforms I work with:\n• **AWS**: SageMaker, EC2, S3\n• **Azure**: ML Studio, Data Factory\n• **GCP**: BigQuery, AI Platform\n\nBenefits: Scalability, cost-efficiency, collaboration\nNeed cloud architecture advice?",

        'automation': "🤖 **Data Science Automation:**\n\nI can automate:\n• Data collection and cleaning\n• Model training and deployment\n• Report generation\n• Monitoring and alerts\n• ETL pipelines\n\nTools: Apache Airflow, Jenkins, Docker\nSave time and reduce errors!",

        'consulting': "💡 **Data Science Consulting:**\n\nI help businesses:\n• Identify data opportunities\n• Develop data strategies\n• Implement solutions\n• Train teams\n• Optimize processes\n\nFrom strategy to implementation - complete data transformation!",
    }

    # Check for keyword matches
    for keyword, response in keywords_responses.items():
        if keyword in user_input_lower:
            return response

    # Name questions
    if any(phrase in user_input_lower for phrase in ['what is your name', 'who are you', 'your name']):
        return "I'm an AI assistant for Adrian! 🤖 I'm here to help you navigate through projects, skills, and services. You can think of me as your personal guide to this portfolio!"

    # Pricing and cost inquiries
    if any(word in user_input_lower for word in ['price', 'cost', 'payment', 'money', 'rate', 'fee', 'charge', 'budget']):
        return "💰 Project pricing depends on complexity and scope:\n\n• Simple data analysis: $20-50\n• Machine learning models: $50-200\n• Full data solutions: $300+\n\nFor an accurate quote, please use the 'Request Project' feature with your specific requirements!"

    # Project and portfolio inquiries
    if any(word in user_input_lower for word in ['project', 'work', 'portfolio', 'example', 'sample']):
        return "🚀 I have several exciting data science projects to show you!\n\n• Machine Learning models\n• Data visualization dashboards\n• Predictive analytics\n• Business intelligence solutions\n\nCheck out the Projects section to see detailed case studies with code, results, and insights!"

    # Skills and technology questions
    if any(word in user_input_lower for word in ['skill', 'technology', 'python', 'machine learning', 'data', 'tool', 'framework']):
        return "🔧 My technical expertise includes:\n\n• Python, R, SQL\n• Machine Learning (scikit-learn, TensorFlow)\n• Data Visualization (Matplotlib, Plotly, Tableau)\n• Big Data (Pandas, NumPy)\n• Cloud platforms (AWS, Azure)\n\nVisit the Skills section for an interactive breakdown!"

    # Contact and communication
    if any(word in user_input_lower for word in ['contact', 'email', 'phone', 'reach', 'talk', 'discuss', 'meeting']):
        return "📞 I'd love to connect with you!\n\n• Email: Available in contact form\n• WhatsApp: For quick questions\n• LinkedIn: Professional networking\n\nI typically respond within 24 hours. Use the Contact page for detailed inquiries!"

    # Experience and background
    if any(word in user_input_lower for word in ['experience', 'background', 'education', 'study', 'degree', 'qualification']):
        return "🎓 I'm currently pursuing a Bachelor of Commerce Honours in Data Science & Informatics.\n\nMy journey includes:\n• Academic projects in ML and analytics\n• Hands-on experience with real datasets\n• Continuous learning in emerging technologies\n\nCheck the About section for my full background!"

    # Blog and learning content
    if any(word in user_input_lower for word in ['blog', 'article', 'read', 'learn', 'tutorial', 'guide']):
        return "📚 I love sharing knowledge! My blog covers:\n\n• Data science tutorials\n• Industry insights\n• Project walkthroughs\n• Technology reviews\n\nVisit the Blog section for the latest articles and learning resources!"

    # Availability and hiring
    if any(word in user_input_lower for word in ['hire', 'freelance', 'available', 'work together', 'collaborate']):
        return "✅ Yes, I'm available for freelance projects and collaborations!\n\nI can help with:\n• Data analysis and insights\n• Machine learning solutions\n• Dashboard development\n• Consulting and training\n\nUse 'Request Project' to discuss your specific needs!"

    # Timeline and duration questions
    if any(word in user_input_lower for word in ['time', 'timeline', 'duration', 'how long', 'when', 'deadline']):
        return "⏰ Project timelines vary by complexity:\n\n• Simple analysis: 1-2 weeks\n• ML models: 2-4 weeks\n• Full solutions: 1-3 months\n\nI always provide detailed timelines during consultation and keep you updated throughout the project!"

    # Help and assistance
    if any(word in user_input_lower for word in ['help', 'assist', 'support', 'guide']):
        return "🤝 I'm here to help! I can assist you with:\n\n• Exploring my projects and skills\n• Understanding my services\n• Answering questions about data science\n• Connecting you with the right resources\n\nWhat specific area would you like to explore?"

    # Technology-specific questions
    if 'python' in user_input_lower:
        return "🐍 Python is my primary language! I use it for:\n\n• Data manipulation (Pandas, NumPy)\n• Machine learning (scikit-learn, TensorFlow)\n• Visualization (Matplotlib, Seaborn)\n• Web development (Django, Flask)\n\nCheck out my Python projects in the portfolio!"

    if any(word in user_input_lower for word in ['machine learning', 'ml', 'ai', 'artificial intelligence']):
        return "🤖 Machine Learning is my passion! I work with:\n\n• Supervised learning (classification, regression)\n• Unsupervised learning (clustering, dimensionality reduction)\n• Deep learning (neural networks)\n• Natural language processing\n\nSee my ML projects for real-world applications!"

    # Database responses
    responses = ChatBotResponse.objects.filter(is_active=True).order_by('-priority')
    for response in responses:
        trigger_words = [word.strip().lower() for word in response.trigger_text.split(',')]
        if response.trigger_type == 'keyword':
            if any(word in user_input_lower for word in trigger_words):
                return response.response_text

    # Enhanced conversational fallbacks with context awareness
    def generate_contextual_response(user_input):
        # Analyze input for context clues
        input_length = len(user_input.split())
        has_question_words = any(word in user_input_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which'])
        has_tech_terms = any(word in user_input_lower for word in ['data', 'analysis', 'model', 'algorithm', 'code', 'programming'])

        if input_length == 1:
            return "🤔 I'd love to help! Could you tell me more about what you're looking for? I can assist with:\n• Data science explanations\n• Project guidance\n• Technology advice\n• Code examples\n• Career insights"

        elif has_question_words and has_tech_terms:
            return "🎯 Great technical question! I can provide detailed explanations about data science topics. Could you be more specific about which aspect you'd like me to cover?"

        elif has_question_words:
            return "❓ I'm here to answer your questions! I specialize in data science topics like:\n• Machine learning concepts\n• Programming techniques\n• Project methodologies\n• Technology recommendations\n• Career guidance\n\nWhat would you like to explore?"

        elif has_tech_terms:
            return "💻 I see you're interested in technical topics! I can dive deep into:\n• Data science technologies\n• Implementation strategies\n• Best practices\n• Code examples\n• Project architectures\n\nWhat specific area interests you?"

        else:
            responses = [
                "🌟 That's interesting! I'm here to help with data science questions and showcase my portfolio. What aspect of data science or my work would you like to explore?",
                "😊 Thanks for reaching out! I'm passionate about data science and love sharing knowledge. Is there a particular topic, project, or service you'd like to learn about?",
                "🚀 I appreciate your message! I'm here to guide you through data science concepts and my portfolio. What would you like to discover today?",
                "💡 Great to connect! I'm specialized in data science and analytics. Whether you need explanations, project ideas, or service information, I'm here to help!",
                "🎯 Hello! I'm your data science assistant, ready to help with technical questions, project guidance, or portfolio exploration. What interests you most?"
            ]

            import random
            return random.choice(responses)

    return generate_contextual_response(user_input)
