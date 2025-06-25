importar prueba unitaria
de biblioteca de rutas importar Camino
de prueba unitaria.imitar importar parche,Simulacro mágico
de núcleo ai.analizador de dependencias importar Analizador de dependencias

clase Analizador de dependencia de pruebas(prueba unitaria.Caso de prueba):
    @método de clase
    definición configurarClase(cls):
        cls.directorio_de_datos_de_prueba = Camino(__archivo__).padre / "datos_de_prueba"
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
        cls.directorio_de_datos_de_prueba.mkdir(existe_ok=Verdadero)
last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py
        
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
        # Crear archivo de prueba con dependencias complejas
        cls.archivo de prueba = cls.directorio_de_datos_de_prueba / "requisitos_muestra.txt"
        con abierto(cls.archivo de prueba,"w")como F:
            F.escribir("numpy>=1.19.0,<2.0.0\nortepandas==1.3.0\norte# Comentario\norte\norte")

    definición configuración(ser):
        ser.analizador = Analizador de dependencias()

last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py
    definición requisitos_de_análisis_de_prueba_txt(ser):
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
        """Prueba para parse_requirements_txt con versiones"""
        resultado = ser.analizador.requisitos_de_análisis_txt(ser.archivo de prueba)
        ser.afirmarIgual(lente(resultado),2)
        ser.afirmarEn("numpy>=1.19.0,<2.0.0",resultado)
        ser.afirmarEn("pandas==1.3.0",resultado)
        ser.assertNotIn("#Comentario",resultado)

last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py
    @parche('subproceso.ejecutar')
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
    definición prueba_obtener_dependencias_del_paquete(ser,ejecución simulada):
        Prueba simulada para _get_package_dependencies
        # Configurar mock
last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py
        resultado simulado = Simulacro mágico()
        resultado simulado.código de retorno = 0
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
        resultado simulado.salida estándar = "Nombre: numpy\norteVersión: 1.21.0\norteRequiere: pandas, scipy
last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py
        ejecución simulada.valor de retorno = resultado simulado
last month
Implementación completa del sistema de pruebas unitarias - Todos los …

        # Ejecutar prueba
        resultado = ser.analizador._obtener_dependencias_del_paquete("numpy")
last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py
        
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
        # Verificar resultados
        ser.afirmarEn("Nombre: numpy",resultado)
        ser.afirmarEn(Versión: 1.21.0,resultado)
        ser.afirmarEn(Requiere: pandas, scipy,resultado)
        ejecución simulada.afirmar_llamado_una_vez_con(['pepita','espectáculo','numpy'],
                                       captura_de_salida=Verdadero,
                                       texto=Verdadero)

    definición método de prueba y análisis(ser):
        """Prueba para el método analizar"""
        ruta de prueba = "/ruta/falsa/al/proyecto"
        resultado = ser.analizador.analizar(ruta de prueba)
        ser.afirmarIgual(resultado["estado"],"éxito")
last month

Crear pruebas/pruebas_unitarias/test_dependency_analyzer.py

si __nombre__ == '__principal__':
last month
Implementación completa del sistema de pruebas unitarias - Todos los …
    prueba unitaria.principal()
