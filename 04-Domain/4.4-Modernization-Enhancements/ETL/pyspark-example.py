from pyspark.sql import SparkSession, SQLContext

if __name__ == '__main__':

    try:

        '''
        PySpark in-memory session example using underlying Java filtering in Container.

        This uses the PySpark SQL library for Joins and Filtering on DataFrames.
        '''

        spark = (
            SparkSession.builder
                .master("local[*]")
                .appName("in-memory-example-session")
                .config("spark.driver.memory", "2g")
                .config("spark.driver.cores", "2")
                .getOrCreate()
        )

        people_df= spark.createDataFrame([
            {"deptId": 1, "age": 40, "name": "Hyukjin Kwon", "gender": "M", "salary": 50},
            {"deptId": 1, "age": 50, "name": "Takuya Ueshin", "gender": "M", "salary": 100},
            {"deptId": 2, "age": 60, "name": "Xinrong Meng", "gender": "F", "salary": 150},
            {"deptId": 3, "age": 20, "name": "Haejoon Lee", "gender": "M", "salary": 200}
        ])
        people_df.show()
        
        department_df = spark.createDataFrame([
            {"id": 1, "name": "PySpark"},
            {"id": 2, "name": "ML"},
            {"id": 3, "name": "Spark SQL"}
        ])   
        department_df.show()     

        # query predicate doesn't use df but entity in df
        people_df \
            .filter(people_df.age >= 35) \
            .join(department_df, people_df.deptId == department_df.id)  \
            .groupBy(department_df.name, "gender")  \
            .agg({"salary": "avg", "age": "max"})  \
            .sort("max(age)")  \
            .show() # this can actually be chained!

        sc = spark.sparkContext # get SQL Context from Session
        parallel_array = sc.parallelize([1, 2, 3, 4, 5])
        print(parallel_array)

        spark.stop()

    except Exception as ex:

        print('Exception: ' + str(ex))
