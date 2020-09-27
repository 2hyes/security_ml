//
//  ViewController.swift
//  FlaskApp
//
//  Created by Sue Cho on 2020/09/19.
//  Copyright © 2020 Sue Cho. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    private let typeOfPreds = ["Normal", "Analysis", "Backdoor", "DoS", "Exploits", "Fuzzers", "Generic", "Reconnaissance", "Shellcodoe", "Worms"]
    private var predsTypeCount = [String : Int]()
    
//    @IBOutlet var resultLabel: UILabel!
    @IBOutlet var getButton: UIButton!
    @IBOutlet var pieChartView: PieChartView!
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.delegate = self
        tableView.dataSource = self
    }

    
    private func receivePredResutFromServer(completion: @escaping ([Int]) -> Void){
        // receive data from the server
        let numberOfFields: Int = 0
        let results: [String] = [""]
        var resultCount = [Int]()
        
        NetworkHelper.shared.getData(numberOfFields: numberOfFields, results: results, completion: { [self] obj in
            guard let receivedResult = obj.results else {
                return
            }
            
            predsTypeCount["Normal"] = receivedResult.filter{ return $0 == "Normal" }.count
            predsTypeCount["Analysis"] = receivedResult.filter{ return $0 == "Analysis" }.count
            predsTypeCount["Backdoor"] = receivedResult.filter{ return $0 == "Backdoor" }.count
            predsTypeCount["DoS"] = receivedResult.filter{ return $0 == "DoS" }.count
            predsTypeCount["Exploits"] = receivedResult.filter{ return $0 == "Exploits" }.count
            predsTypeCount["Fuzzers"] = receivedResult.filter{ return $0 == "Fuzzers" }.count
            predsTypeCount["Generic"] = receivedResult.filter{ return $0 == "Generic" }.count
            predsTypeCount["Reconnaissance"] = receivedResult.filter{ return $0 == "Reconnaissance" }.count
            predsTypeCount["Shellcodoe"] = receivedResult.filter{ return $0 == "Shellcodoe" }.count
            predsTypeCount["Worms"] = receivedResult.filter{ return $0 == "Worms" }.count
            
            let normal = receivedResult.filter { return $0 == "Normal" }
            let abnormal = receivedResult.filter { return $0 != "Normal"}
            resultCount.append(normal.count)
            resultCount.append(abnormal.count)
//            DispatchQueue.main.async {
//                self.resultLabel.text = "\(normal.count) \(abnormal.count)"
//            }
            
            completion(resultCount)
        })
    }
    
    
    @IBAction func getButtonPressed(_ sender: Any) {
        receivePredResutFromServer { (data) in
            let sumOfData = Float(data.reduce(0, +))
            self.pieChartView.slices = [
                Slice(percent: CGFloat( Float(data[0]) / sumOfData ), color: UIColor.blue),
                Slice(percent: CGFloat( Float(data[1]) / sumOfData ), color: UIColor.red)
            ]
            DispatchQueue.main.async {
                self.pieChartView.animateChart()
                self.tableView.reloadData()
            }
        }
    }
    
}

extension ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return typeOfPreds.count
    }
}

extension ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "PredictionCell", for: indexPath) as! PredictionTableViewCell
        
        let attackType: String = typeOfPreds[indexPath.row]
        cell.textLabel?.text = attackType
        cell.detailTextLabel?.text = attackType == "Normal" ? "Normal" : "Attack"
        //cell.textLabel?.text = attackType == "Normal" ? "Normal" : "Attack"
        //cell.detailTextLabel?.text = attackType
        if let count = predsTypeCount[attackType] {
            cell.predictionCountLabel?.text = "\(count)"
        } else { cell.predictionCountLabel?.text = "0" }
        
        return cell
    }
}

class PredictionTableViewCell: UITableViewCell {
    
    @IBOutlet weak var predictionCountLabel: UILabel!
    
}
