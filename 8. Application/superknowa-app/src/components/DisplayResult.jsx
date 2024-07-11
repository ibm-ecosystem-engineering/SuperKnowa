import Result from "./Result";

const DisplayResult = (props) => {
  return (
    <div style={{height: '71vh', overflowY: 'auto', fontSize: "0.875rem",
    lineHeight: "1.5rem", fontWeight: '400', }}>
      {props.results.map((item, i) => (
        <Result 
          typing={true} 
          key={i} 
          question={item.question} 
          answer={item.answer} 
          source={item.source} 
          mongoRef={item.mongoRef}
          model_id={item.model_id}
          type={"single_model"}
          />
      ))}
    </div>
  );
};

export default DisplayResult;
