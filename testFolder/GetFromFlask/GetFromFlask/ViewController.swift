//
//  ViewController.swift
//  GetFromFlask
//
//  Created by Sue Cho on 2020/08/27.
//  Copyright © 2020 Sue Cho. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var dataLabel: UILabel!
    @IBOutlet weak var updateButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func setReceivedData(){
        getPrediction()
    }
    
    
    func getPrediction() {
        
        var request = URLRequest(url: URL(string: "http://127.0.0.1:5000/post")!)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let session = URLSession.shared
        let task = session.dataTask(with: request, completionHandler: { data, response, error -> Void in
            do {
                let json = try JSONSerialization.jsonObject(with: data!) as! Dictionary<String, AnyObject>
                if let respond = json.values.first {
                    print(respond)
                    DispatchQueue.main.async {
                        let sentData = respond as! String
                        self.dataLabel.text = sentData

                    }
                }
                
            } catch {
                print("error")
            }
        })
        
        task.resume()
    }


}

