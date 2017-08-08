public class AlgKMeans {

	public static void execute(){
		
		String train_data = your_dataset /*训练集为二维数组，转换为string类型集合*/
		String cluster_n = k /*聚类类别数*/
		String row = row_of_train_data /*训练集行数*/
		String max_iter = n /*迭代次数*/
		String train_data_result = null; /*加上聚类结果后的train_data*/

		// 聚类结果，返回值为3个所以用长度为3的一维数组
        String rs[] = new String[3];
		try {
            // 设置命令行传入参数，调用python模块，得到返回值（String）保存在train_data_result中
            String[] arg = new String[] { "python", "Users//apple//desktop//test.py", train_data, cluster_n, row, max_iter };
            Process pr = Runtime.getRuntime().exec(arg);
            BufferedReader in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
            String line = null; int i = 0;
            while ((line = in.readLine()) != null) {
            	rs[i] = line; i++;
            }
            train_data_result = rs[2];
            in.close();
            pr.waitFor();

        } catch (Exception e) {
            e.printStackTrace();
        } 

		// 解析train_data_result
		List<String> list = new ArrayList<String>();
		String str[] = train_data_result.split("],");
		for (int i = 0; i < str.length; i++){
			str[i] = str[i].replace("[","").replace("]", "").replace(" ", "");
			list.add(str[i]);
		}
		
		// 将str转为rdd
		JavaRDD<String> rdd = JavaSparkContext.fromSparkContext(df.sqlContext().sparkContext()).parallelize(list);
		JavaRDD<Row> personsRDD = rdd.map(new Function<String,Row>(){
            public Row call(String line) throws Exception {
            	//System.out.println(line);
                String[] splited = line.split(",");
                return RowFactory.create(Double.valueOf(splited[0]),Double.valueOf(splited[1]),
                		Double.valueOf(splited[2]),Double.valueOf(splited[3]),
                		Double.valueOf(splited[4]),Double.valueOf(splited[5]),
                		Double.valueOf(splited[6]),Double.valueOf(splited[7]),
                		Double.valueOf(splited[8]),Double.valueOf(splited[9]),
                		Double.valueOf(splited[10]),Integer.valueOf(splited[11]));
            }
        });

		// rdd转dataframe
		List<StructField> fields = new ArrayList<StructField>();
		fields.add(DataTypes.createStructField("X", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("Y", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("FFMC", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("DMC", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("DC", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("ISI", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("temp", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("RH", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("wind", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("rain", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("area", DataTypes.DoubleType, true));
		fields.add(DataTypes.createStructField("prediction", DataTypes.IntegerType, true));
		StructType schema = DataTypes.createStructType(fields);	
		DataFrame cluster = df.sqlContext().createDataFrame(personsRDD, schema);
	
	}
}