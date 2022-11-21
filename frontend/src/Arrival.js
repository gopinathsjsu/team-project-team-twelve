import React from "react";
import './App.css';
class Arrival extends React.Component {

	// Constructor
	constructor(props) {
		super(props);

		this.state = {
			items: [],
			DataisLoaded: false
		};
	}


	// ComponentDidMount is used to
	// execute the code
	async componentDidMount() {
        const url = "https://6369fe7ac07d8f936d901493.mockapi.io/getArrivals";
// 		fetch(
// "https://jsonplaceholder.typicode.com/users")
// 			.then((res) => res.json())
// 			.then((json) => {
// 				this.setState({
// 					items: json,
// 					DataisLoaded: true
// 				});
// 			})
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        this.setState({ items: data.Arrivals, DataisLoaded: true });
	}
	render() {
		const { DataisLoaded, items } = this.state;
		if (!DataisLoaded) return <div>
			<h1> Pleses wait sometime.... </h1> </div> ;
        
        return (
            <>
            <div className = "App-header">
                <h1> ARRIVALS </h1>  
                {
                    items.map((item) => (
                    <li key = { item.id } >
                        {item.airline}, 
                        {item.flight_code}, 
                        {item.timestamp}
                        <button>View Details</button>
                    </li>
                    ))
                }
            </div>
            </>
        );
        // function viewDetails (e){

        // }
		// return (
        //     <> <h1 > ARRIVALS </h1>
		//     <div className = "App-header">
		// 	{
		// 		items.map((item) => (
        //             return <Item key={item.id} item={item} />
		// 		// <li key = { item.id } >
		// 		// 	User_Name: { item.username },
		// 		// 	Full_Name: { item.name },
		// 		// 	User_Email: { item.email }
        //         //     <button onClick={viewDetails}>View Details</button>
		// 		// 	</li>
		// 		))
		// 	}
		// </div>
        // </>
	// );
}
}


export default Arrival;
