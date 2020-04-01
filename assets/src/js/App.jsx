import React,{useEffect} from 'react';
import { Widget ,addResponseMessage,  toggleWidget} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
export default () => {
    useEffect(()=>{toggleWidget()},[])
    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        addResponseMessage("You just said: "+ newMessage);
        
        // Now send the message throught the backend API
    }
    return (
        <Widget
            title='oSocrates'
            subtitle='Talk to your colleague about this issue...'
            handleNewUserMessage={handleNewUserMessage}
        />

    )
}

