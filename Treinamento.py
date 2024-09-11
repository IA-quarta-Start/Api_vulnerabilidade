import joblib
from sklearn.svm import SVC
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd

# Exemplo de dados de treinamento
base_dados = pd.read_csv('base_padronizada.csv')

# Separar previsores (X) e classe (y)
X = base_dados.drop(columns=['vulnerabilidade_social'])
y = base_dados['vulnerabilidade_social']

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definindo as colunas categóricas e numéricas
categorical_features = X.select_dtypes(include=['object']).columns
numeric_features = X.select_dtypes(include=['float64']).columns

# Pipelines para pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=True), categorical_features)
    ]
)

# Pipeline final
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', SVC())
])

# Treinar o modelo
model.fit(X_train, y_train)

# Salvar o modelo
joblib.dump(model, 'modelo_treinado.pkl')

# Fazer previsões
y_pred = model.predict(X_test)

# Calcular a acurácia
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia: {accuracy:.2f}')

# Gerar a matriz de confusão
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
print('Matriz de Confusão:')
print(cm)

# Exibir a matriz de confusão de forma gráfica
cmd = ConfusionMatrixDisplay(cm, display_labels=model.classes_)
cmd.plot(cmap='Blues')
